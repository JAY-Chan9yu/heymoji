import re
import requests
import json
from dataclasses import dataclass
from operator import itemgetter
from app import crud
from app.schemas import UserCreate, SlackEventHook
from app.models import User
from app.settings import REACTION_LIST, DAY_MAX_REACTION, SLACKTOKEN, SLACK_CHANNEL

# about reaction
REMOVED_REACTION = 'reaction_removed'
ADDED_REACTION = 'reaction_added'
APP_MENTION_REACTION = 'app_mention'

# about command
CREATE_USER_COMMAND = 'create_user'
SHOW_THIS_MONTH_PRISE = '칭찬을 보여줘'


@dataclass
class EventDto:
    type: str  # ex: reaction_added
    user: str  # 리액션을 한 유저(slack_id)
    item: dict  # type, channel, ts
    reaction: str  # 리액션(이모지)
    item_user: str  # 리액션을 받은 유저(slack_id)
    event_ts: str
    text: str  # app mention text

    def __init__(self, event_data):
        self.type = event_data.get('type')
        self.user = event_data.get('user')
        self.item = event_data.get('item')
        self.reaction = event_data.get('reaction')
        self.item_user = event_data.get('item_user')
        self.event_ts = event_data.get('event_ts')
        self.text = event_data.get('text')


@dataclass
class AddUserCommandDto:
    name: str
    slack_id: str
    avatar_url: str

    def __init__(self, name: str, slack_id: str, avatar_url: str):
        self.name = name.strip('name=')
        self.slack_id = slack_id.strip('slack_id=')
        self.avatar_url = avatar_url.strip('avatar_url=')


class SlackService:

    @classmethod
    def check_challenge(cls, event: SlackEventHook, db) -> dict:
        # slack Enable Events
        if 'challenge' in event:
            return {"challenge": event['challenge']}

        # check slack event
        if "event" in event:
            event_dto = EventDto(event['event'])

            if event_dto.type in [ADDED_REACTION, REMOVED_REACTION]:
                # 다른 사람에게만 이모지 줄 수 있음
                if event_dto.item_user != event_dto.user:
                    cls.assign_emoji(event_dto, db)
            elif event_dto.type == APP_MENTION_REACTION:
                cls.manage_app_mention(event_dto, db)

        return {}

    @classmethod
    def assign_emoji(cls, event: EventDto, db):
        """
        reaction process
        """
        if event.reaction not in REACTION_LIST:
            return

        if event.type == ADDED_REACTION:
            user = crud.get_user(db, event.user)
            # 멤버에게 줄 수 있는 나의 reaction 개수 체크
            if user.my_reaction > 0:
                crud.update_my_reaction(db, user, False)
                crud.update_added_reaction(db=db, type=event.reaction, item_user=event.item_user,
                                           user=event.user, is_increase=True)

        elif event.type == REMOVED_REACTION:
            user = crud.get_user(db, event.user)
            # 멤버에게 전달한 reaction을 삭제하는 경우 (이미 하루 최대의 reaction 개수인 경우 더이상 추가하지 않음)
            if user.my_reaction < DAY_MAX_REACTION:
                crud.update_my_reaction(db, user, True)
                crud.update_added_reaction(db=db, type=event.reaction, item_user=event.item_user,
                                           user=event.user, is_increase=False)

    @classmethod
    def manage_app_mention(cls, event: EventDto, db):
        """
        명령어를 분기 처리하는 함수
        ex: <@ABCDEFG> --create_user --name=JAY --slack_id=ABCDEFG --avatar_url=https://blablac.com/abcd

        오늘의 칭찬 리스트를 return
        ex: <@ABCDEFG> -- 오늘의 칭찬을 보여줘 --
        """

        event_command = event.text.split('--')
        print('event_commnet', event_command)
        event_command.pop(0)  # 첫번째 값은 user slack_id
        if not event_command:
            return

        _type = event_command.pop(0).strip(' ')

        if _type == CREATE_USER_COMMAND:
            if len(event_command) == 3:
                add_user_cmd_dto = AddUserCommandDto(event_command[0], event_command[1], event_command[2])
                cls.add_user(add_user_cmd_dto, db)

        elif SHOW_THIS_MONTH_PRISE in _type:
            # 2021년 8월의 칭찬을 보여줘
            year = re.sub(r'[^0-9]', '', _type.split(' ')[0])
            month = re.sub(r'[^0-9]', '', _type.split(' ')[1])

            # 숫자로 변환 try 해보고 안되면 return
            try:
                year = int(year)
                month = int(month)
                prise_list = cls.show_this_month_prise(year, month, db)
                cls.send_prise_msg_to_slack(_type, prise_list)
            except:
                return

    @classmethod
    def add_user(cls, add_user_cmd_dto: AddUserCommandDto, db):
        """
        user 추가 명령어
        """
        db_user = crud.get_user(db, item_user=add_user_cmd_dto.slack_id)
        if db_user:
            return

        user = UserCreate(username=add_user_cmd_dto.name, slack_id=add_user_cmd_dto.slack_id,
                          using_emoji_count=DAY_MAX_REACTION, get_emoji_count=0,
                          avatar_url=add_user_cmd_dto.avatar_url)
        crud.create_user(db=db, user=user)

    @classmethod
    def show_this_month_prise(cls, year: int, month: int, db):
        """
        이번 달 최고 멤버들 뽑기
        member_reaction_list = [{'username' : '김병욱', 'love' : 3, 'funny' : 5, 'help' : 5, 'good' : 10, 'bad' : 5},{'username' : '김병욱', 'love' : 3, 'funny' : 5, 'help' : 5, 'good' : 10, 'bad' : 5}]
        """
        user_list = db.query(User).all()

        member_reaction_list = []
        for user in user_list:
            get_member_reaction = crud.get_member_reaction_count(db, user, year, month)
            member_reaction_list.append(get_member_reaction)

        # 각각의 best member 뽑기
        best_love = sorted(member_reaction_list, key=itemgetter('love'))[-1]['username']
        best_funny = sorted(member_reaction_list, key=itemgetter('funny'))[-1]['username']
        best_help = sorted(member_reaction_list, key=itemgetter('help'))[-1]['username']
        best_good = sorted(member_reaction_list, key=itemgetter('good'))[-1]['username']
        best_bad = sorted(member_reaction_list, key=itemgetter('bad'))[-1]['username']

        prise_list = dict(best_love=best_love, best_funny=best_funny, best_help=best_help, best_good=best_good, best_bad=best_bad)

        return prise_list

    @classmethod
    def send_prise_msg_to_slack(cls, title, prise_list):
        token = SLACKTOKEN

        title = '칭찬봇아 ~~ ' + title
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*{}*".format(title)
                }
            },
            {
                "type": "section",
                "block_id": "section567",
                "text": {
                    "type": "mrkdwn",
                    "text": "이번 달 가장 많은 사랑을 받은 크루는?! {} :heart: ".format(prise_list.get('best_love'))
                },
                "accessory": {
                    "type": "image",
                    "image_url": "https://i.pinimg.com/originals/bf/88/4c/bf884cb9b29803db712b77f1bce4f462.jpg",
                    "alt_text": "Haunted hotel image"
                }
            },
            {
                "type": "section",
                "block_id": "section568",
                "text": {
                    "type": "mrkdwn",
                    "text": "이번 달 개그맨 보다 더 많은 웃음을 준 크루는?! {} :kkkk: :기쁨: ".format(prise_list.get('best_funny'))
                },
                "accessory": {
                    "type": "image",
                    "image_url": "https://t1.daumcdn.net/cfile/tistory/99E10D3F5ADC079602",
                    "alt_text": "Haunted hotel image"
                }
            },
            {
                "type": "section",
                "block_id": "section569",
                "text": {
                    "type": "mrkdwn",
                    "text": "이번 달 많은 크루를 도와준 천사 크루는?! {} :pray: :기도: ".format(prise_list.get('best_help'))
                },
                "accessory": {
                    "type": "image",
                    "image_url": "http://images.goodoc.kr/images/article/2018/08/20/428733/43bedd6ad60a_3bbaf99a964d.png",
                    "alt_text": "Haunted hotel image"
                }
            },
            {
                "type": "section",
                "block_id": "section570",
                "text": {
                    "type": "mrkdwn",
                    "text": "이번 달 가장 많은 이슈를 처리해 준 크루는?! {} :+1: :wow: :wonderfulk: :천재_개발자:".format(prise_list.get('best_good'))
                },
                "accessory": {
                    "type": "image",
                    "image_url": "https://cdn.clien.net/web/api/file/F03/11193449/82140da86eecc4.jpg?w=500&h=1000",
                    "alt_text": "Haunted hotel image"
                }
            },
            {
                "type": "section",
                "block_id": "section571",
                "text": {
                    "type": "mrkdwn",
                    "text": "이번 달 가장 많은 크루를 당황시킨 크루는?! {} :eye_shaking: ".format(prise_list.get('best_bad'))
                },
                "accessory": {
                    "type": "image",
                    "image_url": "https://d2u3dcdbebyaiu.cloudfront.net/uploads/atch_img/693/6ebb2cf8ed8a3f6cdebe2f6aedc640e6.jpeg",
                    "alt_text": "Haunted hotel image"
                }
            }
        ]

        cls.post_message(token, SLACK_CHANNEL, blocks=blocks)

    @classmethod
    def post_message(cls, token, channel, blocks):
        requests.post(
            "https://slack.com/api/chat.postMessage",
            headers={"Authorization": "Bearer "+token, "Content-Type": "application/json"},
            data=json.dumps({"channel": channel, "blocks": blocks})
        )

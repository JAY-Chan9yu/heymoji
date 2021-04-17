from dataclasses import dataclass

from app import crud
from app.schemas import UserCreate, SlackEventHook

from app.settings import REACTION_LIST, DAY_MAX_REACTION

# about reaction
REMOVED_REACTION = 'reaction_removed'
ADDED_REACTION = 'reaction_added'
APP_MENTION_REACTION = 'app_mention'

# about command
CREATE_USER_COMMAND = 'create_user'


@dataclass
class EventDto:
    type: str # ex: reaction_added
    user: str # 리액션을 한 유저(slack_id)
    item: dict # type, channel, ts
    reaction: str # 리액션(이모지)
    item_user: str # 리액션을 받은 유저(slack_id)
    event_ts: str
    text: str # app mention text

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


class SlackService(object):

    def check_challenge(self, event: SlackEventHook, db) -> dict:
        # slack Enable Events
        if 'challenge' in event:
            return {"challenge": event['challenge']}

        # check slack event
        if "event" in event:
            event_dto = EventDto(event['event'])

            if event_dto.type in [ADDED_REACTION, REMOVED_REACTION]:
                # 다른 사람에게만 이모지 줄 수 있음
                if event_dto.item_user != event_dto.user:
                    self.assign_emoji(event_dto, db)
            elif event_dto.type == APP_MENTION_REACTION:
                self.manage_app_mention(event_dto, db)

        return {}

    def assign_emoji(self, event: EventDto, db):
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

    def manage_app_mention(self, event: EventDto, db):
        """
        명령어를 분기 처리하는 함수
        ex: <@ABCDEFG> --create_user --name=JAY --slack_id=ABCDEFG --avatar_url=https://blablac.com/abcd
        """
        event_command = event.text.split('--')
        event_command.pop(0) # 첫번째 값은 user slack_id
        if not event_command:
            return

        _type = event_command.pop(0).strip(' ')

        if _type == CREATE_USER_COMMAND:
            if len(event_command) == 3:
                add_user_cmd_dto = AddUserCommandDto(event_command[0], event_command[1], event_command[2])
                self.add_user(add_user_cmd_dto, db)


    def add_user(self, add_user_cmd_dto: AddUserCommandDto, db):
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

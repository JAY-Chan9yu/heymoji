from dataclasses import dataclass

from pydantic.main import BaseModel

from models.users import crud
from models.users.schemas import UserCreate, SlackEventHook

# about reaction
REACTION = 'heart'
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
class CommandDto:
    type: str
    cmd: str

    def __init__(self, _type: str, cmd: str):
        self.type = _type
        self.cmd = cmd


@dataclass
class AddUserCommandDto:
    user_name: str
    slack_id: str

    def __init__(self, user_name: str, slack_id: str):
        self.user_name = user_name
        self.slack_id = slack_id


class SlackService(object):

    def check_challenge(self, event: SlackEventHook, db) -> dict:
        # slack Enable Events
        if 'challenge' in event:
            return {"challenge": event['challenge']}

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
        if event.reaction != REACTION:
            return

        if event.type == ADDED_REACTION:
            user = crud.get_user(db, event.user)
            # 다른사람에게 이모지 줄 수 있는 카운트 남아 있는지 체크
            if user.using_emoji_count > 0:
                crud.update_using_emoji_count(db, user, False)
                crud.update_get_emoji(db, event.item_user, True)

        elif event.type == REMOVED_REACTION:
            user = crud.get_user(db, event.user)
            # 이모지 추가한걸 취소한 경우
            if user.using_emoji_count < 5:
                crud.update_using_emoji_count(db, user, True)
                crud.update_get_emoji(db, event.item_user, False)

    def manage_app_mention(self, event: EventDto, db):
        # ex: ['<@ABCDFEFG>', 'create_user', 'jay-ABCDEFGS']
        mention_data = event.text.split(' ')
        if len(mention_data) < 3:
            return

        cmd_dto = CommandDto(_type=mention_data[1], cmd=mention_data[2])
        if cmd_dto.type == CREATE_USER_COMMAND:
            self.add_user(cmd_dto.cmd, db)

    def add_user(self, cmd: str, db):
        command = cmd.split('-')
        if len(command) < 2:
            return

        add_cmd_dto = AddUserCommandDto(user_name=command[0], slack_id=command[1])
        db_user = crud.get_user(db, item_user=add_cmd_dto.slack_id)
        if db_user:
            return

        user = UserCreate(username=add_cmd_dto.user_name, slack_id=add_cmd_dto.slack_id,
                          using_emoji_count=5, get_emoji_count=0)
        crud.create_user(db=db, user=user)

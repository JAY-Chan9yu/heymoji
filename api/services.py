from dataclasses import dataclass

from pydantic.main import BaseModel

from models.users import crud

REACTION = 'heart'
REMOVED_REACTION = 'reaction_removed'
ADDED_REACTION = 'reaction_added'


class SlackEventHook(BaseModel):
    token: str
    team_id: str
    api_app_id: str
    event: dict
    type: str
    event_id: str
    event_time: int
    authorizations: list
    is_ext_shared_channel: bool
    event_context: str


@dataclass
class EventDto:
    type: str # ex: reaction_added
    user: str # 리액션을 한 유저(slack_id)
    item: dict # type, channel, ts
    reaction: str # 리액션(이모지)
    item_user: str # 리액션을 받은 유저(slack_id)
    event_ts: str

    def __init__(self, event_data):
        self.type = event_data.get('type')
        self.user = event_data.get('user')
        self.item = event_data.get('item')
        self.reaction = event_data.get('reaction')
        self.item_user = event_data.get('item_user')
        self.event_ts = event_data.get('event_ts')


class SlackService(object):

    def check_challenge(self, event: SlackEventHook, db) -> dict:
        # slack Enable Events
        if 'challenge' in event:
            return {"challenge": event['challenge']}

        if "event" in event:
            event_dto = EventDto(event['event'])
            # 다른 사람에게만 이모지 줄 수 있음
            if event_dto.item_user != event_dto.user:
                self.assign_emoji(event_dto, db)

        return {}

    def assign_emoji(self, event: EventDto, db):
        if event.reaction != REACTION:
            return

        if event.type == ADDED_REACTION:
            user = crud.get_user(db, event.user)
            # 다른사람에게 이모지 줄 수 있는 카운트 남아 있는지 체크
            if user.using_emoji_count > 1:
                crud.update_using_emoji_count(db, user, False)
                crud.update_get_emoji(db, event.item_user, True)

        elif event.type == REMOVED_REACTION:
            user = crud.get_user(db, event.user)
            # 이모지 추가한걸 취소한 경우
            if user.using_emoji_count < 5:
                crud.update_using_emoji_count(db, user, True)
                crud.update_get_emoji(db, event.item_user, False)

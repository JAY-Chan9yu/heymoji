from dataclasses import dataclass

from pydantic.main import BaseModel

from models.users import crud

REACTION_TYPE = 'heart'


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
            self.increase_emoji_count(event_dto, db)

        return {}

    def increase_emoji_count(self, event: EventDto, db):
        if event.reaction == REACTION_TYPE:
            crud.update_user(db, event.item_user)
        return {}

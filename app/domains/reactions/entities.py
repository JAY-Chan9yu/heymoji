from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from app.domains.users.entities import User
from seed_work.entities import AggregateRoot


class SlackEventType(Enum):
    REMOVED_REACTION = 'reaction_removed'
    ADDED_REACTION = 'reaction_added'
    APP_MENTION_REACTION = 'app_mention'
    APP_MESSAGE = 'message'


class Reaction(AggregateRoot):
    year: int = Field(title='년')
    month: int = Field(title='월')
    emoji: str = Field(title='이모지')
    count: int = Field(title='이모지 카운트', default=1)
    to_user_id: int = Field(title='리액션 받은 사람 ID')
    from_user_id: int = Field(title='리액션 준 사람 ID')

    to_user: Optional[User] = Field(title='리액션 받은 사람', default=None)
    from_user: Optional[User] = Field(title='리액션 준 사람', default=None)

    def __init__(self, **kwargs):
        if kwargs.get('to_user'):
            kwargs['to_user'] = User(**kwargs['to_user'].__dict__)

        if kwargs.get('from_user'):
            kwargs['from_user'] = User(**kwargs['from_user'].__dict__)

        super().__init__(**kwargs)

    def entity_to_data(self) -> dict:
        data = self.__dict__
        data.pop('id')
        data.pop('to_user')
        data.pop('from_user')
        return data

    def update_count(self, event_type: SlackEventType):
        if event_type not in [SlackEventType.ADDED_REACTION, SlackEventType.REMOVED_REACTION]:
            return

        if event_type == SlackEventType.ADDED_REACTION:
            self.increase_count()
        elif event_type == SlackEventType.REMOVED_REACTION:
            self.decrease_count()

    def decrease_count(self):
        if self.count > 0:
            self.count -= 1

    def increase_count(self):
        self.count += 1


class ReceivedEmojiInfo(BaseModel):
    emoji: str
    count: int


class UserReceivedEmojiInfo(BaseModel):
    username: str
    emoji_infos: List[ReceivedEmojiInfo] = []

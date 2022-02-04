from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from app.domains.users.entities import User
from seed_work.entities import AggregateRoot


class ReactionType(Enum):
    REMOVED_REACTION = 'reaction_removed'
    ADDED_REACTION = 'reaction_added'
    APP_MENTION_REACTION = 'app_mention'
    APP_MESSAGE = 'message'


class Reaction(AggregateRoot):
    year: int = Field(title='년')
    month: int = Field(title='월')
    type: str = Field(title='이모지 타입')
    count: int = Field(title='이모지 카운트')
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

    def update_count(self, event_type: str):
        is_increase = True if event_type == ReactionType.ADDED_REACTION.value else False

        if is_increase:
            self.increase_count()
        else:
            self.decrease_count()

    def decrease_count(self):
        if self.count > 0:
            self.count -= 1

    def increase_count(self):
        self.count += 1


class ReactionCreate(BaseModel):
    year: int
    month: int
    to_user: int
    from_user: int
    type: str


class ReceivedEmojiInfo(BaseModel):
    type: str
    count: int


class UserReceivedEmojiInfo(BaseModel):
    username: str
    emoji: List[ReceivedEmojiInfo] = []

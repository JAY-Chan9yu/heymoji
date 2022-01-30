from enum import Enum
from typing import List, Optional

from pydantic import BaseModel

from app.domain.schemas.user_schema import User


class ReactionType(Enum):
    REMOVED_REACTION = 'reaction_removed'
    ADDED_REACTION = 'reaction_added'
    APP_MENTION_REACTION = 'app_mention'
    APP_MESSAGE = 'message'


class BaseReaction(BaseModel):
    id: Optional[int]
    year: int
    month: int
    type: str
    count: int


class ReactionMeta(BaseReaction):
    """
    Reaction Table 과 일치하는 스키마
    """
    to_user_id: int
    from_user_id: int


class Reaction(BaseReaction):
    to_user: User
    from_user: User

    def __init__(self, **kwargs):
        if kwargs.get('to_user'):
            kwargs['to_user'] = User(**kwargs['to_user'].__dict__)

        if kwargs.get('from_user'):
            kwargs['from_user'] = User(**kwargs['from_user'].__dict__)

        super().__init__(**kwargs)


class ReactionCreate(BaseModel):
    year: int
    month: int
    to_user: int
    from_user: int
    type: str


class ReceivedEmojiInfo(BaseModel):
    type: str
    count: int


# # todo: response schema 로 분리
class UserReceivedEmojiInfo(BaseModel):
    username: str
    emoji: List[ReceivedEmojiInfo] = []

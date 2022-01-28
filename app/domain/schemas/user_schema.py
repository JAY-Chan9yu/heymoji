from typing import List, Optional
from pydantic import BaseModel

from app.domain.schemas.reaction_schema import ReceivedEmojiInfo


class BaseUser(BaseModel):
    id: int
    username: str
    avatar_url: Optional[str]


class User(BaseUser):
    slack_id: str


class UserDetailInfo(BaseUser):
    my_reaction: int = 0
    received_reaction_count: int


# todo: response schema 로 분리
class UserReceivedReactions(BaseModel):
    username: str
    emoji: List[ReceivedEmojiInfo]

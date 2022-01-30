from typing import Optional
from pydantic import BaseModel


class BaseUser(BaseModel):
    id: Optional[int]
    username: str
    avatar_url: Optional[str]


class User(BaseUser):
    slack_id: str
    my_reaction: int = 0


class UserDetailInfo(BaseUser):
    my_reaction: int = 0
    received_reaction_count: int

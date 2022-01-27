from typing import List

from pydantic import BaseModel


# about User
class User(BaseModel):
    id: int
    username: str
    slack_id: str
    my_reaction: int

    class Config:
        orm_mode = True


class ReceivedReactionUser(BaseModel):
    id: int
    avatar_url: str
    username: str
    my_reaction: int
    received_reaction: int


class UserCreate(BaseModel):
    username: str
    slack_id: str
    avatar_url: str


class UserReaction(BaseModel):
    username: str
    slack_id: str
    avatar_url: str
    my_reaction: int
    total_reaction: int


# about Reaction
class Reaction(BaseModel):
    id: int
    year: int
    month: int
    to_user: int
    from_user: int
    type: str
    count: int

    class Config:
        orm_mode = True


class ReactionCreate(BaseModel):
    year: int
    month: int
    to_user: int
    from_user: int
    type: str


class ReceivedEmojiInfo(BaseModel):
    type: str
    count: int


class UserReceivedReactions(BaseModel):
    username: str
    emoji: List[ReceivedEmojiInfo]


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

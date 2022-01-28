from pydantic import BaseModel


class Reaction(BaseModel):
    id: int
    year: int
    month: int
    to_user: int
    from_user: int
    type: str
    count: int


class ReactionCreate(BaseModel):
    year: int
    month: int
    to_user: int
    from_user: int
    type: str


class ReceivedEmojiInfo(BaseModel):
    type: str
    count: int

from pydantic import BaseModel


class UserBase(BaseModel):
    slack_id: str


class UserCreate(BaseModel):
    username: str
    slack_id: str
    get_emoji_count: int
    using_emoji_count: int


class User(UserBase):
    id: int
    username: str
    get_emoji_count: int
    using_emoji_count: int

    class Config:
        orm_mode = True

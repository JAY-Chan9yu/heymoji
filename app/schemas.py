from pydantic import BaseModel


class UserBase(BaseModel):
    slack_id: str


class UserCreate(BaseModel):
    username: str
    slack_id: str
    get_emoji_count: int
    using_emoji_count: int
    avatar_url: str


class User(UserBase):
    id: int
    username: str
    get_emoji_count: int
    using_emoji_count: int

    class Config:
        orm_mode = True


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

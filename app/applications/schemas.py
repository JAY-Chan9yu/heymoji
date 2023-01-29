from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from conf import settings


class CommandType(Enum):
    HELP_COMMAND = 'help'
    CREATE_USER_COMMAND = 'create_user'
    UPDATE_USER_COMMAND = 'update_user'
    HIDE_USER_COMMAND = 'hide_user'
    SHOW_USER_COMMAND = 'show_user'
    SHOW_BEST_MEMBER_COMMAND = 'show_best_member'


class SlackEvent(BaseModel):
    type: str = Field(title='리액션 타입')
    user: str = Field(title='리액션을 한 유저(slack_id)')
    item_user: str = Field(title='리액션을 받은 유저(slack_id)')
    reaction: str = Field(title='리액션(이모지)')
    text: Optional[str] = Field(title='app mention text', default=None)
    channel: Optional[str] = Field(title='이벤트 발생한 채널', default=settings.config.ERROR_CHANNEL)
    event_ts: str
    item: dict  # type, channel, ts


class SlackMentionEvent(BaseModel):
    type: str = Field(title='리액션 타입')
    user: str = Field(title='리액션을 한 유저(slack_id)')
    text: Optional[str] = Field(title='app mention text', default=None)
    channel: Optional[str] = Field(title='이벤트 발생한 채널', default=settings.config.ERROR_CHANNEL)
    event_ts: str


class SlackBotEvent(SlackMentionEvent):
    """slack bot direct message event"""
    bot_profile: Optional[dict] = None


class BaseSlackEventHook(BaseModel):
    token: str
    team_id: str = Field(title='워크스페이스 아이디')
    api_app_id: str = Field(title='애플리케이션 아이디')
    type: str = Field(title='이벤트 타입')
    event_id: str = Field(title='이벤트 아이디')
    event_time: int = Field(title='이벤트 발생 시간')
    is_ext_shared_channel: bool
    event_context: str = Field(title='이벤트 식별자')
    authorizations: list = Field(title='인증서')


class SlackEventHook(BaseSlackEventHook):
    """슬랙 이벤트 웹훅 스키마"""
    event: SlackEvent = Field(title='이벤트 상세')


class SlackMentionHook(BaseSlackEventHook):
    """슬랙 멘션 이벤트 웹훅 스키마"""
    event: SlackMentionEvent = Field(title='이벤트 상세')


class SlackBotDirectMessageHook(BaseSlackEventHook):
    """슬랙 봇 다이렉트 메세지 웹훅 스키마"""
    event: SlackBotEvent = Field(title='이벤트 상세')


class SlackChallengeHook(BaseModel):
    """
    슬랙 웹훅 연결 테스트를 위한 스키마
    """
    token: str
    challenge: str
    type: str


class SlackChallengeHookResponse(BaseModel):
    challenge: str

from pydantic import BaseModel, Field


class SlackEventHook(BaseModel):
    token: str
    team_id: str = Field(title='워크스페이스 아이디')
    api_app_id: str = Field(title='애플리케이션 아이디')
    event: dict = Field(title='이벤트 상세')
    type: str = Field(title='이벤트 타입')
    event_id: str = Field(title='이벤트 아이디')
    event_time: int = Field(title='이벤트 발생 시간')
    is_ext_shared_channel: bool
    event_context: str = Field(title='이벤트 식별자')
    authorizations: list = Field(title='인증서')


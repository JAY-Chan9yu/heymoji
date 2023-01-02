from typing import Optional

from pydantic import BaseModel, Field

from conf import settings


class UserCreateSchema(BaseModel):
    slack_id: str
    name: str
    avatar_url: Optional[str] = Field(default=settings.config.DEFAULT_AVATAR_URL)
    department: Optional[str] = Field(default="개그팀")

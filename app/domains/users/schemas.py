from typing import Optional

from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    slack_id: str
    username: str
    avatar_url: Optional[str]
    department: Optional[str]

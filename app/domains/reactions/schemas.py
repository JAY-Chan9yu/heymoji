from pydantic import BaseModel


class ReactionCreate(BaseModel):
    year: int
    month: int
    to_user: int
    from_user: int
    emoji: str

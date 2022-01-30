from typing import Optional

from app.domain.schemas.user_schema import User
from app.repositories.user_repository import UserRepository


class UserService:
    _user_repository = UserRepository

    @classmethod
    async def get_detail_user_by_year_and_month(cls, year: Optional[int] = None, month: Optional[int] = None):
        return await cls._user_repository().get_detail_user_by_year_and_month(year, month)

    @classmethod
    async def get_users(cls):
        return await cls._user_repository().get_users()

    @classmethod
    async def get_user(cls, slack_id: str):
        return await cls._user_repository().get_user(slack_id)

    @classmethod
    async def create_user(cls, user: User):
        return await cls._user_repository().create_user(user)

    @classmethod
    async def update_user(cls, user: User):
        return await cls._user_repository().update_user(user)

    @classmethod
    async def update_my_reaction(cls, user: User, is_increase: bool):
        return await cls._user_repository().update_my_reaction(user, is_increase)

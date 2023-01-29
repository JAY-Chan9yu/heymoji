from typing import List, Optional

from app.domains.users.entities import User
from app.domains.users.services import UserService


class UserAppService:
    _user_domain_service = UserService

    @classmethod
    async def get_user(cls, slack_id: str) -> Optional[User]:
        return await cls._user_domain_service.get_by_slack_id(slack_id=slack_id)

    @classmethod
    async def get_detail_user(
        cls,
        year: Optional[int] = None,
        month: Optional[int] = None,
        department: Optional[str] = None
    ):
        return await cls._user_domain_service.get_detail_user(
            year=year,
            month=month,
            department=department
        )

    @classmethod
    async def get_all_users(cls) -> List[User]:
        return await cls._user_domain_service.get_all_users()

    @classmethod
    async def create_user(cls, attr: dict):
        return await cls._user_domain_service.create_user(attr)

    @classmethod
    async def update_user(cls, attr: dict):
        await cls._user_domain_service.update_user(attr)

    @classmethod
    async def hide_user(cls, attr: dict):
        await cls._user_domain_service.hide_user(attr)

    @classmethod
    async def show_user(cls, attr: dict):
        await cls._user_domain_service.show_user(attr)

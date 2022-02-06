from typing import List, Optional

from app.domains.users.entities import User
from app.domains.users.services import UserService


class UserAppService:
    _user_domain_service = UserService

    @classmethod
    async def update_today_assigned_reaction_count(cls, user: User, is_increase: bool):
        """
        오늘 유저에게 할당된 리액션 (다른 유저에게)줄 수 있는 카운트 업데이트
        """
        await cls._user_domain_service.update_my_reaction(user, is_increase)

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
        await cls._user_domain_service.create_user(attr)

    @classmethod
    async def update_user(cls, attr: dict):
        await cls._user_domain_service.update_user(attr)

    @classmethod
    async def hide_user(cls, attr: dict):
        await cls._user_domain_service.hide_user(attr)

    @classmethod
    async def show_user(cls, attr: dict):
        await cls._user_domain_service.show_user(attr)

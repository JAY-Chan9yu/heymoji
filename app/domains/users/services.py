import logging
from contextlib import asynccontextmanager
from typing import Optional, List

from app.domains.users.entities import User, UserDetailInfo
from app.domains.users.repositories import UserRepository
from conf import settings


logger = logging.getLogger(__name__)


class UserService:
    _user_repository = UserRepository

    @classmethod
    async def get_by_slack_id(cls, slack_id: str) -> Optional[User]:
        return await cls._user_repository().get_by_slack_id(slack_id)

    @classmethod
    async def get_by_id(cls, _id: int) -> Optional[User]:
        return await cls._user_repository().get_by_id(_id)

    @classmethod
    async def get_detail_user(cls, **kwargs) -> List[UserDetailInfo]:
        return await cls._user_repository().get_detail_info(**kwargs)

    @classmethod
    async def get_all_users(cls) -> List[User]:
        return await cls._user_repository().get_all_users()

    @classmethod
    async def create_user(cls, attr: dict) -> User:
        user = await cls.get_by_slack_id(slack_id=attr['slack_id'])
        if user:
            return user

        return await cls._user_repository().insert(User(
            username=attr.get('name'),
            slack_id=attr.get('slack_id'),
            avatar_url=attr.get('avatar_url', settings.config.DEFAULT_AVATAR_URL),
            department=attr.get('department', '개그팀'),
        ))

    @classmethod
    async def update_user(cls, attr: dict):
        async with user_check_manager(attr) as user:
            user.update_attr(**attr)
            await cls._user_repository().update(user)

    @classmethod
    async def hide_user(cls, attr: dict):
        async with user_check_manager(attr) as user:
            user.hide_user()
            await cls._user_repository().update(user)

    @classmethod
    async def show_user(cls, attr: dict):
        async with user_check_manager(attr) as user:
            user.show_user()
            await cls._user_repository().update(user)


@asynccontextmanager
async def user_check_manager(attr):
    user = await UserService.get_by_slack_id(slack_id=attr['slack_id'])

    try:
        yield user
    except Exception as e:
        logger.error(f"[user_check_manager] {e}")
        return

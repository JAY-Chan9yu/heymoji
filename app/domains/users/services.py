from contextlib import asynccontextmanager
from typing import Optional, List

from app.domains.users.entities import User
from app.domains.users.repositories import UserRepository


class UserService:
    _user_repository = UserRepository

    @classmethod
    async def get_by_slack_id(cls, slack_id: str) -> Optional[User]:
        return await cls._user_repository().get_by_slack_id(slack_id)

    @classmethod
    async def get_by_id(cls, _id: int):
        return await cls._user_repository().get_by_id(_id)

    @classmethod
    async def get_detail_user(cls, **kwargs):
        return await cls._user_repository().get_detail_info(**kwargs)

    @classmethod
    async def get_all_users(cls) -> List[User]:
        return await cls._user_repository().get_all_users()

    @classmethod
    async def create_user(cls, attr: dict):
        user = await cls.get_by_slack_id(slack_id=attr['slack_id'])
        if user:
            return

        return await cls._user_repository().insert(User(
            username=attr.get('name'),
            slack_id=attr.get('slack_id'),
            avatar_url=attr.get('avatar_url'),
            department=attr.get('department'),
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

    @classmethod
    async def update_my_reaction(cls, user: User, is_increase: bool):
        user.decrease_my_reaction() if is_increase else user.increase_my_reaction()
        return await cls._user_repository().update(user)


@asynccontextmanager
async def user_check_manager(attr):
    if not attr.get('slack_id'):
        return

    user = await UserService.get_by_slack_id(slack_id=attr['slack_id'])

    try:
        yield user
    except Exception as err:
        print(err)
        return

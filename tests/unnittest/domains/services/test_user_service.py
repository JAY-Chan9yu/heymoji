from typing import List

import pytest

from app.domains.users.entities import User, UserDetailInfo
from app.domains.users.repositories import UserModel
from app.domains.users.services import UserService
from tests.conftest import truncate_tables, test_engine
from tests.helpers.model_factories import UserModelFactory
from tests.helpers.randoms import get_random_string
from tests.helpers.user_creator import create_random_users


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
class TestUserService:
    def setup_class(self):
        self.user: UserModel = UserModelFactory(test_engine).build()
        self.service = UserService()

    def teardown_class(self):
        truncate_tables(["users", "reactions"])

    @pytest.mark.asyncio
    async def test_get_user_by_id(self, db, anyio_backend):
        user: User = await self.service.get_by_slack_id(slack_id=self.user.slack_id)
        assert user is not None
        assert user.id == self.user.id
        assert user.slack_id == self.user.slack_id

    @pytest.mark.asyncio
    async def test_get_by_id(self, db, anyio_backend):
        user: User = await self.service.get_by_id(_id=self.user.id)
        assert user is not None
        assert user.id == self.user.id
        assert user.slack_id == self.user.slack_id

    @pytest.mark.asyncio
    async def test_get_detail_user(self, db, anyio_backend):
        new_user: UserModel = UserModelFactory(test_engine).build(**{
            "slack_id": "abcdefg",
            "username": "test-new-user",
            "avatar_url": "yoyo",
            "department": "detail-gag-team"
        })
        detail_info = {
            "department": "detail-gag-team"
        }
        users: List[UserDetailInfo] = await self.service.get_detail_user(**detail_info)
        assert len(users) == 1
        assert users[0].id == new_user.id

    @pytest.mark.asyncio
    async def test_get_all_users(self, db, anyio_backend):
        truncate_tables(["users", "reactions"])
        create_random_users(10)
        users: List[User] = await self.service.get_all_users()
        assert len(users) == 10

    @pytest.mark.asyncio
    async def test_create_user(self, db, anyio_backend):
        user: User = await self.service.create_user(attr={
            "slack_id": get_random_string(),
            "name": "test-new-user",
            "avatar_url": "yoyo",
            "department": "gag-team"
        })
        assert user is not None

    @pytest.mark.asyncio
    async def test_create_exists_user(self, db, anyio_backend):
        slack_id = get_random_string()
        UserModelFactory(test_engine).build(**{
            "slack_id": slack_id,
            "username": "test-new-user",
            "avatar_url": "yoyo",
            "department": "gag-team"
        })
        user = await self.service.create_user(attr={
            "slack_id": slack_id,
            "username": "test-new-user",
            "avatar_url": "yoyo",
            "department": "gag-team"
        })
        assert user is None

    @pytest.mark.asyncio
    async def test_update_user(self, db, anyio_backend):
        slack_id = get_random_string()
        user_data = {
            "slack_id": slack_id,
            "username": "test-new-user",
            "avatar_url": "yoyo",
            "department": "gag-team"
        }
        UserModelFactory(test_engine).build(**user_data)
        user: User = await self.service.get_by_slack_id(slack_id=slack_id)
        assert user.username == user_data["username"]
        assert user.avatar_url == user_data["avatar_url"]
        assert user.department == user_data["department"]

        updated_user_data = {
            "slack_id": slack_id,
            "name": "update-user-name",
            "avatar_url": "updated-avatar-url",
            "department": "updated-gag-team"
        }
        await self.service.update_user(attr=updated_user_data)
        user: User = await self.service.get_by_slack_id(slack_id=slack_id)
        assert user.username == updated_user_data["name"]
        assert user.avatar_url == updated_user_data["avatar_url"]
        assert user.department == updated_user_data["department"]

    @pytest.mark.asyncio
    async def test_hide_user_and_show_user(self, db, anyio_backend):
        slack_id = get_random_string()
        user_data = {
            "slack_id": slack_id,
            "username": "test-new-user",
            "avatar_url": "yoyo",
            "department": "gag-team"
        }
        UserModelFactory(test_engine).build(**user_data)
        user: User = await self.service.get_by_slack_id(slack_id=slack_id)
        assert user.is_display is True

        await self.service.hide_user({"slack_id": slack_id})
        user: User = await self.service.get_by_slack_id(slack_id=slack_id)
        assert user.is_display is False

        await self.service.show_user({"slack_id": slack_id})
        user: User = await self.service.get_by_slack_id(slack_id=slack_id)
        assert user.is_display is True

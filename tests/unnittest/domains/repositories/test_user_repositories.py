import pytest

from app.domains.users.entities import User, UserDetailInfo
from app.domains.users.repositories import UserRepository, UserModel
from tests.conftest import truncate_tables, test_engine
from tests.helpers.model_factories import UserModelFactory


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
class TestUserRepository:
    def setup_class(self):
        self.user: UserModel = UserModelFactory(test_engine).build()
        self.repository = UserRepository()

    def teardown_class(self):
        truncate_tables(["users", "reactions"])

    @pytest.mark.asyncio
    async def test_get_user_by_id(self, anyio_backend):
        user = await self.repository.get_by_id(_id=self.user.id)
        assert user is not None
        assert user.id == self.user.id
        assert user.slack_id == self.user.slack_id
        assert user.department == self.user.department
        assert user.avatar_url == self.user.avatar_url
        assert user.is_display == self.user.is_display

    @pytest.mark.asyncio
    async def test_get_user_by_slack_id(self, anyio_backend):
        user = await self.repository.get_by_slack_id(slack_id=self.user.slack_id)
        assert user is not None
        assert user.id == self.user.id
        assert user.slack_id == self.user.slack_id
        assert user.department == self.user.department
        assert user.avatar_url == self.user.avatar_url
        assert user.is_display == self.user.is_display

    @pytest.mark.asyncio
    async def test_get_all_users(self, anyio_backend):
        users = await self.repository.get_all_users()
        assert len(users) == 1
        assert users[0].id == self.user.id
        assert users[0].slack_id == self.user.slack_id
        assert users[0].department == self.user.department
        assert users[0].avatar_url == self.user.avatar_url
        assert users[0].is_display == self.user.is_display

    @pytest.mark.asyncio
    async def test_insert(self, anyio_backend):
        user_data = {
            "slack_id": "abcdefg",
            "username": "test-new-user",
            "avatar_url": "yoyo",
            "department": "omg"
        }
        await self.repository.insert(User(**user_data))
        user = await self.repository.get_by_slack_id(slack_id=user_data['slack_id'])
        assert user is not None
        assert user.slack_id == user_data['slack_id']
        assert user.department == user_data['department']
        assert user.avatar_url == user_data['avatar_url']
        assert user.is_display is True

    @pytest.mark.asyncio
    async def test_get_detail_info(self, anyio_backend):
        detail_info = {
            "department": "gag-team"
        }
        users = await self.repository.get_detail_info(**detail_info)
        assert len(users) == 1
        assert isinstance(users[0], UserDetailInfo)

        user_data = {
            "slack_id": "detail-info-user",
            "username": "new-user",
            "avatar_url": "yoyo",
            "department": "gag-team"
        }
        await self.repository.insert(User(**user_data))
        users = await self.repository.get_detail_info(**detail_info)
        assert len(users) == 2

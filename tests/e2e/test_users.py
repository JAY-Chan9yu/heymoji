import json

import pytest

from app.domains.users.repositories import UserModel
from tests.conftest import truncate_tables, test_engine
from tests.helpers.model_factories import ReactionModelFactory, UserModelFactory
from tests.helpers.randoms import get_random_string
from tests.helpers.user_creator import create_random_users


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
class TestUserApi:
    def setup_class(self):
        self.user: UserModel = UserModelFactory(test_engine).build()
        self.other_user: UserModel = UserModelFactory(test_engine).build(**{
            "slack_id": get_random_string(20),
            "username": "test-new-user",
            "avatar_url": "yoyo",
            "department": "gag-team"
        })

    def teardown_class(self):
        truncate_tables(["users", "reactions"])

    @pytest.mark.asyncio
    async def test_get_users(self, db, anyio_backend, test_client):
        create_random_users(10)
        response = await test_client.get("/users/")
        assert response.status_code == 200
        data = json.loads(response.text)
        assert len(data) == 12  # self.user + self.other_user

    @pytest.mark.asyncio
    async def test_create_users(self, db, anyio_backend, test_client):
        payload = {
            "slack_id": get_random_string(20),
            "name": "jay",
            "avatar_url": "url",
            "department": "gag-team"
        }
        response = await test_client.post("/users/", json=payload)
        assert response.status_code == 200
        data = json.loads(response.text)
        assert data["slack_id"] == payload["slack_id"]
        assert data["username"] == payload["name"]
        assert data["avatar_url"] == payload["avatar_url"]
        assert data["department"] == payload["department"]

    @pytest.mark.asyncio
    async def test_create_exists_users(self, db, anyio_backend, test_client):
        payload = {
            "slack_id": self.user.slack_id,
            "name": "jay",
            "avatar_url": "url",
            "department": "gag-team"
        }
        response = await test_client.post("/users/", json=payload)
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_get_reactions(self, db, anyio_backend, test_client):
        truncate_tables(["reactions"])

        emoji = get_random_string(5)
        ReactionModelFactory(db).build(
            to_user_id=self.user.id,
            from_user_id=self.other_user.id,
            emoji=emoji
        )
        ReactionModelFactory(db).build(
            to_user_id=self.user.id,
            from_user_id=self.other_user.id,
            emoji='other-emoji'
        )
        ReactionModelFactory(db).build(
            to_user_id=self.user.id,
            from_user_id=self.other_user.id,
            emoji=emoji,
            year=1991,
            month=9
        )
        ReactionModelFactory(db).build(
            to_user_id=self.user.id,
            from_user_id=self.other_user.id,
            emoji=emoji,
            year=1991,
            month=8
        )

        response = await test_client.get(f"/users/{self.user.id}/reactions/")
        assert response.status_code == 200
        data = json.loads(response.text)
        assert data[0]["username"] == self.other_user.username
        assert len(data[0]["emoji_infos"]) == 2
        assert data[0]["emoji_infos"][0]["emoji"] == emoji
        assert data[0]["emoji_infos"][0]["count"] == 3
        assert data[0]["emoji_infos"][1]["emoji"] == 'other-emoji'
        assert data[0]["emoji_infos"][1]["count"] == 1

        response = await test_client.get(f"/users/{self.user.id}/reactions/", params={"year": 1991, "month": 9})
        assert response.status_code == 200
        data = json.loads(response.text)
        assert data[0]["username"] == self.other_user.username
        assert len(data[0]["emoji_infos"]) == 1
        assert data[0]["emoji_infos"][0]["emoji"] == emoji
        assert data[0]["emoji_infos"][0]["count"] == 1

    @pytest.mark.asyncio
    async def test_get_my_reaction(self, db, anyio_backend, mock_allowed_emoji, test_client):
        truncate_tables(["reactions"])
        for _ in range(0, 5):
            ReactionModelFactory(db).build(
                to_user_id=self.user.id,
                from_user_id=self.other_user.id,
                emoji="heart"
            )
        response = await test_client.get(f"/users/{self.user.slack_id}/my_reaction/")
        assert response.status_code == 200
        data = json.loads(response.text)
        assert data["❤️"] == 5

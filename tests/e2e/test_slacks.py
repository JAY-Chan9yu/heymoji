import json

import pytest

from app.domains.users.repositories import UserModel
from tests.conftest import truncate_tables, test_engine
from tests.helpers.model_factories import UserModelFactory
from tests.helpers.randoms import get_random_string


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
class TestSlackApi:
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
    async def test_slack_handler_by_challenge(self, db, anyio_backend, test_client, mock_challenge_request):
        response = await test_client.post("/slack/")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_slack_handler_by_direct_message(
        self, db, anyio_backend, test_client, mock_bot_direct_message_request
    ):
        response = await test_client.post("/slack/")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_slack_handler_by_add_reacton(self, db, anyio_backend, mock_allowed_emoji, test_client):
        truncate_tables(["reactions"])
        body = {
            "event": {
                "type": "reaction_added",
                "user": self.other_user.slack_id,
                "item_user": self.user.slack_id,
                "text": get_random_string(20),
                "channel": get_random_string(5),
                "event_ts": "1609878469.036400",
                "reaction": "heart",
                "item": {},
            },
            "bot_id": "ABCDEFG",
            "type": "message",
            "text": "Test message",
            "user": "12345678",
            "ts": "1609878469.036400",
            "team": "jay-team",
            "token": get_random_string(10),
            "team_id": get_random_string(10),
            "api_app_id": get_random_string(10),
            "event_id": get_random_string(10),
            "event_time": 1609878469,
            "is_ext_shared_channel": True,
            "event_context": get_random_string(10),
            "authorizations": []
        }
        response = await test_client.post("/slack/", json=body)
        assert response.status_code == 200

        response = await test_client.get(f"/users/{self.user.id}/reactions/")
        assert response.status_code == 200
        data = json.loads(response.text)
        assert data[0]["username"] == self.other_user.username
        assert len(data[0]["emoji_infos"]) == 1
        assert data[0]["emoji_infos"][0]["emoji"] == "heart"
        assert data[0]["emoji_infos"][0]["count"] == 1

    # @pytest.mark.asyncio
    # async def test_slack_handler_by_add_reacton_when_limited_special_emoji(
    #     self, db, anyio_backend, mock_allowed_emoji, mock_reaction_list, test_client
    # ):
    #     truncate_tables(["reactions"])
    #     body = {
    #         "event": {
    #             "type": "reaction_added",
    #             "user": self.other_user.slack_id,
    #             "item_user": self.user.slack_id,
    #             "text": get_random_string(20),
    #             "channel": get_random_string(5),
    #             "event_ts": "1609878469.036400",
    #             "reaction": "special",
    #             "item": {},
    #         },
    #         "bot_id": "ABCDEFG",
    #         "type": "message",
    #         "text": "Test message",
    #         "user": "12345678",
    #         "ts": "1609878469.036400",
    #         "team": "jay-team",
    #         "token": get_random_string(10),
    #         "team_id": get_random_string(10),
    #         "api_app_id": get_random_string(10),
    #         "event_id": get_random_string(10),
    #         "event_time": 1609878469,
    #         "is_ext_shared_channel": True,
    #         "event_context": get_random_string(10),
    #         "authorizations": []
    #     }
    #     for _ in range(0, 10):
    #         response = await test_client.post("/slack/", json=body)
    #         assert response.status_code == 200
    #
    #     response = await test_client.get(f"/users/{self.user.id}/reactions/")
    #     assert response.status_code == 200
    #     data = json.loads(response.text)
    #     assert data[0]["emoji_infos"][0]["emoji"] == "special"
    #     assert data[0]["emoji_infos"][0]["count"] == 5

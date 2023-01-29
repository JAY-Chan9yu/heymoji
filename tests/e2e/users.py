import pytest

from app.domains.users.repositories import UserModel
from tests.conftest import test_engine, truncate_tables


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
class TestCreatePerson:

    def teardown_method(self):
        truncate_tables(["users", "reactions"])

    async def test_root(self, db, anyio_backend, test_client):
        payload = {
            "slack_id": "123122222223",
            "name": "j44422ay",
            "avatar_url": "이미지 URL",
            "department": "개그팀"
        }
        response = await test_client.post("/slack/", json=payload)
        assert response.status_code == 200
        response = await test_client.post("/users/", json=payload)
        assert response.status_code == 400

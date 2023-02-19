import os
from typing import List
from unittest import mock

import httpx
import pytest
from asyncio import get_event_loop

import pytest_asyncio
from asgi_lifespan import LifespanManager
from sqlalchemy import create_engine

from app.main import app

from alembic.config import Config as AlembicConfig
from alembic.command import upgrade as alembic_upgrade

from conf import settings
from tests.helpers.randoms import get_random_string

test_mysql_url = f'mysql+pymysql://{settings.config.DB_USERNAME}:{settings.config.DB_PASSWORD}' \
                 f'@{settings.config.DB_HOST}:{settings.config.DB_PORT}'
test_engine = create_engine(test_mysql_url, echo=True)


def truncate_tables(tables: List[str]):
    test_engine.execute("USE test_heymoji")
    test_engine.execute("SET FOREIGN_KEY_CHECKS = 0")
    for table in tables:
        test_engine.execute(f"TRUNCATE TABLE {table}")
    test_engine.execute("SET FOREIGN_KEY_CHECKS = 1")


@pytest.fixture(scope='session', autouse=True)
def db():
    print('\n----- CREATE TEST DB CONNECTION POOL AND CREATE DATABASE\n')
    test_engine.execute("CREATE DATABASE IF NOT EXISTS test_heymoji")
    test_engine.execute("USE test_heymoji")

    print('\n----- RUN ALEMBIC MIGRATION\n')
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    alembic_config = AlembicConfig(os.path.join(root_dir, 'alembic.ini'))
    alembic_config.set_main_option('sqlalchemy.url', test_mysql_url + f'/{settings.config.DATABASE}')
    alembic_config.set_main_option("script_location", os.path.join(root_dir, 'migrations'))
    alembic_upgrade(alembic_config, 'head')

    yield test_engine

    print('\n----- RELEASE TEST DB CONNECTION POOL AND DROP DATABASE\n')
    test_engine.execute("DROP DATABASE test_heymoji")
    test_engine.dispose()


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    """using same event_loop for async test"""
    loop = get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(params=[
    pytest.param(('asyncio', {'use_uvloop': True}), id='asyncio+uvloop'),
    pytest.param(('asyncio', {'use_uvloop': False}), id='asyncio'),
    pytest.param(('trio', {'restrict_keyboard_interrupt_to_checkpoints': True}), id='trio')
])
def anyio_backend(request):
    """choice backend async library for async"""
    # https://anyio.readthedocs.io/en/stable/testing.html#specifying-the-backends-to-run-on
    return request.param


@pytest_asyncio.fixture
async def test_client():
    async with LifespanManager(app):
        async with httpx.AsyncClient(app=app, base_url="http://heymoji") as client:
            yield client


@pytest.fixture(scope='function')
def mock_allowed_emoji():
    with mock.patch(
        'app.domains.reactions.services.settings.config.ALLOWED_EMOJI_TYPES',
        [
            {"emoji": "❤️", "emoji_names": ["heart"]},
            {"emoji": "🤣", "emoji_names": ["kkkk"]},
            {"emoji": "🙏️", "emoji_names": ["pray"]},
            {"emoji": "👍", "emoji_names": ["+1"]},
            {"emoji": "👀️", "emoji_names": ["eye_shaking"]},
            {"emoji": "⭐️️", "emoji_names": ["special"]}
        ]
    ) as allowed_emoji:
        yield allowed_emoji


@pytest.fixture(scope='function')
def mock_reaction_list():
    with mock.patch(
        'app.applications.services.slack_services.settings.config.ALLOWED_REACTION_LIST',
        ["pray", "heart", "eye_shaking", "+1", "kkkk", "special"]
    ) as reaction_list:
        yield reaction_list


@pytest.fixture(scope='function')
def mock_challenge_request():
    with mock.patch(
        'app.api.dependency.requests.Request.json',
        return_value={
            "challenge": get_random_string(20),
            "token": get_random_string(20),
            "type": "http"
        }
    ) as mock_request_body:
        yield mock_request_body


@pytest.fixture(scope='function')
def mock_bot_direct_message_request():
    with mock.patch(
        'app.api.dependency.requests.Request.json',
        return_value={
            "event": {
                "bot_profile": {
                    "ts": "1609878469.036400",
                    "id": "ABCDEFG",
                    "deleted": False,
                    "name": "my-bot-name",
                    "updated": 1608584973,
                    "app_id": "<omitted>",
                    "icons": {
                        "image_36": "...",
                        "image_48": "...",
                        "image_72": "..."
                    },
                    "team_id": "abc1234"
                },
                "event_ts": "1609878469.036400",
                "type": "mention",
                "user": get_random_string(),
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
    ) as mock_bot_direct_message_body:
        yield mock_bot_direct_message_body


@pytest.fixture(scope='function')
def mock_slack_mention_request():
    with mock.patch(
        'app.api.dependency.requests.Request.json',
        return_value={
            "event": {
                "type": "app_mention",
                "user": get_random_string(),
                "text": get_random_string(20),
                "channel": get_random_string(5),
                "event_ts": "1609878469.036400",
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
    ) as mock_slack_mention_body:
        yield mock_slack_mention_body


@pytest.fixture(scope='function')
def mock_slack_evnet_request():
    with mock.patch(
        'app.api.dependency.requests.Request.json',
        return_value={
            "event": {
                "type": "reaction_added",
                "user": get_random_string(),
                "item_user": get_random_string(),
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
    ) as mock_slack_mention_body:
        yield mock_slack_mention_body

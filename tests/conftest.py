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

test_mysql_url = f'mysql+pymysql://{settings.config.DB_USERNAME}:{settings.config.DB_PASSWORD}' \
                 f'@{settings.config.DB_HOST}:{settings.config.DB_PORT}'
test_engine = create_engine(test_mysql_url, echo=True)


def truncate_tables(tables: List[str]):
    test_engine.execute("USE test_heymoji")
    test_engine.execute("SET FOREIGN_KEY_CHECKS = 0")
    for table in tables:
        test_engine.execute(f"TRUNCATE TABLE {table}")
    test_engine.execute("SET FOREIGN_KEY_CHECKS = 1")


@pytest.fixture(scope='function')
def mock_allowed_emoji():
    with mock.patch(
        'app.domains.reactions.services.settings.config.ALLOWED_EMOJI_TYPES',
        [
            {"emoji": "❤️", "emoji_names": ["heart"]},
            {"emoji": "🤣", "emoji_names": ["kkkk"]},
            {"emoji": "🙏️", "emoji_names": ["pray"]},
            {"emoji": "👍", "emoji_names": ["+1"]},
            {"emoji": "👀️", "emoji_names": ["eye_shaking"]}
        ]
    ) as allowed_emoji:
        yield allowed_emoji


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

from contextlib import asynccontextmanager
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base, Session

from conf import settings


Base = declarative_base()
_async_db_connection: AsyncEngine = Optional[AsyncEngine]
_db_connection: Engine = Optional[Engine]


def on_startup():
    # todo: 동기, 비동기 하나만 사용하도록 조건 넣기 or 환경변수 주입으로?
    global _async_db_connection
    global _db_connection

    _async_db_connection = create_async_engine(
        f'mysql+aiomysql://{settings.config.DB_USERNAME}:{settings.config.DB_PASSWORD}'
        f'@{settings.config.DB_HOST}:{settings.config.DB_PORT}/{settings.config.DATABASE}',
        echo=True if settings.config.ENV != settings.HeymojiEnv.PROD.value else False,
        future=True
    )

    _db_connection = create_engine(
        f'mysql+pymysql://{settings.config.DB_USERNAME}:{settings.config.DB_PASSWORD}'
        f'@{settings.config.DB_HOST}:{settings.config.DB_PORT}/{settings.config.DATABASE}',
        echo=True if settings.config.ENV != settings.HeymojiEnv.PROD.value else False,
        # connect_args={"check_same_thread": False}
    )


def on_shutdown():
    global _async_db_connection
    global _db_connection

    if _async_db_connection:
        _async_db_connection.dispose()

    if _db_connection:
        _db_connection.dispose()


class MysqlConnectionManager:
    _client = None

    @classmethod
    def get_connection(cls, is_async: bool):
        if cls._client is None:
            if is_async:
                cls._client = scoped_session(sessionmaker(
                    autocommit=False,
                    autoflush=False,
                    bind=_async_db_connection,
                    class_=AsyncSession(bind=_async_db_connection, expire_on_commit=True)
                ))
            else:
                cls._client = scoped_session(sessionmaker(
                    autocommit=False,
                    autoflush=False,
                    bind=_db_connection,
                    class_=Session
                ))

        return cls._client


@asynccontextmanager
async def async_session_manager() -> AsyncSession:
    session = AsyncSession(bind=_async_db_connection, expire_on_commit=True)

    try:
        yield session
        await session.commit()
    except Exception as err:
        await session.rollback()
        print(err)
    finally:
        await session.close()
        # await async_engine.dispose()

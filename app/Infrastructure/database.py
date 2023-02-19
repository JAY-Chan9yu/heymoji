from contextlib import asynccontextmanager
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base, Session

from conf import settings


Base = declarative_base()
async_db_connection: Optional[AsyncEngine] = None
db_connection: Optional[Engine] = None

db_url = f"{settings.config.DB_USERNAME}:{settings.config.DB_PASSWORD}" \
         f"@{settings.config.DB_HOST}:{settings.config.DB_PORT}/{settings.config.DATABASE}"


def on_startup():
    # todo: 동기, 비동기 하나만 사용하도록 조건 넣기 or 환경변수 주입으로?
    global async_db_connection
    global db_connection

    async_db_connection = create_async_engine(
        f'mysql+aiomysql://{db_url}',
        echo=True if settings.config.ENV != settings.HeymojiEnv.PROD.value else False,
        future=True
    )

    db_connection = create_engine(
        f'mysql+pymysql://{db_url}',
        echo=True if settings.config.ENV != settings.HeymojiEnv.PROD.value else False,
        # connect_args={"check_same_thread": False}
    )


def on_shutdown():
    global async_db_connection
    global db_connection

    if async_db_connection:
        async_db_connection.dispose()

    if db_connection:
        db_connection.dispose()


class MysqlConnectionManager:
    _client = None

    @classmethod
    def get_connection(cls, is_async: bool):
        if cls._client is None:
            if is_async:
                cls._client = scoped_session(sessionmaker(
                    autocommit=False,
                    autoflush=False,
                    bind=async_db_connection,
                    class_=AsyncSession(bind=async_db_connection, expire_on_commit=True)
                ))
            else:
                cls._client = scoped_session(sessionmaker(
                    autocommit=False,
                    autoflush=False,
                    bind=db_connection,
                    class_=Session
                ))

        return cls._client


@asynccontextmanager
async def async_session_manager() -> AsyncSession:
    global async_db_connection

    if not async_db_connection:
        async_db_connection = create_async_engine(
            f'mysql+aiomysql://{db_url}',
            echo=True if settings.config.ENV != settings.HeymojiEnv.PROD.value else False,
            future=True
        )

    session = AsyncSession(bind=async_db_connection, expire_on_commit=True)

    try:
        yield session
        await session.commit()
    except Exception as err:
        await session.rollback()
        print(err)
    finally:
        await session.close()
        # await async_engine.dispose()

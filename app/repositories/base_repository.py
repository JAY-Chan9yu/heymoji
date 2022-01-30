from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base, Session

from conf import settings


Base = declarative_base()


class BaseRepository:
    _client = None

    @classmethod
    def get_connection(cls, is_async: bool):
        if cls._client is None:
            """
            비동기로 db connection 을 처리하려면 scoped_session 을 사용하면 안된다.
            참고: https://blog.neonkid.xyz/266
            """
            if is_async:
                engine = create_async_engine(
                    f'mysql+aiomysql://{settings.config.USERNAME}:{settings.config.PASSWORD}'
                    f'@{settings.config.HOST}:{settings.config.PORT}/{settings.config.DATABASE}',
                    future=True, echo=True
                )
                # todo: asyncio scoped session 가 필요한가?
                # https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#using-asyncio-scoped-session
                cls._client = AsyncSession(bind=engine, expire_on_commit=False)

            else:
                engine = create_engine(
                    f'mysql+pymysql://{settings.config.USERNAME}:{settings.config.PASSWORD}'
                    f'@{settings.config.HOST}:{settings.config.PORT}/{settings.config.DATABASE}',
                    connect_args={"check_same_thread": False}
                )  # echo="debug" )

                cls._client = scoped_session(sessionmaker(
                    autocommit=False, autoflush=False, bind=engine, class_=Session
                ))

        return cls._client

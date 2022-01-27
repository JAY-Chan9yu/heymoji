from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

from conf import settings


Base = declarative_base()


class BaseRepository:
    _client = None

    @classmethod
    def get_connection(cls):
        """
        비동기로 db connection 을 처리하려면 scoped_session 을 사용하면 안된다.
        참고: https://blog.neonkid.xyz/266
        """
        if cls._client is None:
            engine = create_engine(
                f'mysql+pymysql://{settings.config.USERNAME}:{settings.config.PASSWORD}'
                f'@{settings.config.HOST}:{settings.config.PORT}/{settings.config.DATABASE}'
            )  #echo="debug" )
            cls._client = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        return cls._client

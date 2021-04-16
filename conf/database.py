from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from conf.config import Settings

settings = Settings(_env_file='prod.env')
DB_URL = f'mysql+pymysql://{settings.USERNAME}:{settings.PASSWORD}' \
         f'@{settings.HOST}:{settings.PORT}/{settings.DATABASE}'
engine = create_engine(DB_URL, echo="debug")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

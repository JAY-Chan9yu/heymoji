from abc import ABC, abstractmethod
from contextlib import contextmanager
from datetime import datetime

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from app.domains.reactions.repositories import ReactionModel
from app.domains.users.repositories import UserModel
from tests.helpers.randoms import get_random_string


class AbstractModelFactory(ABC):

    def __init__(self, db: Engine):
        self.db = db

    @abstractmethod
    def build(self, *args, **kwargs):
        ...


class UserModelFactory(AbstractModelFactory):

    def build(self, **kwargs) -> UserModel:
        user = UserModel(
            username=kwargs.get("username", "jay-ji"),
            slack_id=kwargs.get("slack_id", get_random_string()),
            avatar_url=kwargs.get("avatar_url", "test_url"),
            department=kwargs.get("department", "gag-team"),
            is_display=True
        )
        with session_manager(self.db) as session:
            session.add(user)
            session.commit()
            session.close()
        return user


class ReactionModelFactory(AbstractModelFactory):

    def build(self, to_user_id: int, from_user_id: int, **kwargs) -> ReactionModel:
        now = datetime.now()
        reaction = ReactionModel(
            to_user_id=to_user_id,
            from_user_id=from_user_id,
            year=kwargs.get("year", now.year),
            month=kwargs.get("month", now.month),
            emoji=kwargs.get("emoji", "heart"),
            count=1
        )
        with session_manager(self.db) as session:
            session.add(reaction)
            session.commit()
            session.close()
        return reaction


@contextmanager
def session_manager(db) -> Session:
    session = Session(bind=db, expire_on_commit=False)

    try:
        yield session
        session.commit()
    except Exception as err:
        session.rollback()
        print(err)
    finally:
        session.close()
        # await async_engine.dispose()

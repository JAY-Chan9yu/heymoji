from typing import Optional

from app.repositories.user_repository import UserRepository


class UserService:
    _user_repository = UserRepository

    @classmethod
    def get_user_list(cls, year: Optional[int] = None, month: Optional[int] = None):
        return cls._user_repository().get_users(year, month)

    @classmethod
    def get_user(cls, slack_id: str):
        return cls._user_repository().get_user(slack_id)

    @classmethod
    def create_user(cls, user):
        return cls._user_repository().create_user(user)

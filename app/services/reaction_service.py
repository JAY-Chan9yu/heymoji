from typing import Optional

from app.domain.schemas.user_schema import User
from app.repositories.reaction_repository import ReactionRepository


class ReactionService:
    _reaction_repository = ReactionRepository

    @classmethod
    def get_user_reactions(cls, user_id: int, year: Optional[int] = None, month: Optional[int] = None):
        return cls._reaction_repository().get_reactions(user_id, year, month)

    @classmethod
    def get_my_reaction(cls, slack_id: str, year: Optional[int] = None, month: Optional[int] = None):
        return cls._reaction_repository().get_my_reaction(slack_id, year, month)

    @classmethod
    def update_added_reaction(cls, reaction_type: str, item_user: str, user: str, is_increase: bool):
        return cls._reaction_repository().update_added_reaction(reaction_type, item_user, user, is_increase)

    @classmethod
    def update_my_reaction(cls, user: User, is_increase: bool):
        return cls._reaction_repository().update_my_reaction(user, is_increase)

    @classmethod
    def get_member_reaction_count(cls, user: User, year: int, month: int):
        return cls._reaction_repository().get_member_reaction_count(user, year, month)

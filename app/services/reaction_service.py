from typing import Optional

from app.domain.schemas.reaction_schema import ReactionType, ReactionMeta, UserReceivedEmojiInfo, ReceivedEmojiInfo
from app.domain.schemas.slack_schema import SlackEvent
from app.domain.schemas.user_schema import User
from app.repositories.reaction_repository import ReactionRepository
from app.services.user_service import UserService
from conf import settings


class ReactionService:
    _reaction_repository = ReactionRepository
    _user_service = UserService

    @classmethod
    async def update_user_reaction(cls, event: SlackEvent, user: User):
        if event.reaction not in settings.config.REACTION_LIST:
            return

        is_increase = True if event.type == ReactionType.ADDED_REACTION.value else False
        await cls._user_service.update_my_reaction(user, False)
        await cls.update_reaction(
            reaction_type=event.reaction,
            received_user_slack_id=event.item_user,
            send_user_slack_id=event.user,
            is_increase=is_increase
        )

    @classmethod
    async def get_user_reactions(cls, user_id: int, year: Optional[int] = None, month: Optional[int] = None):
        return await cls._reaction_repository().get_reactions(user_id, year, month)

    @classmethod
    async def get_my_reaction(cls, slack_id: str, year: Optional[int] = None, month: Optional[int] = None) -> dict:
        reaction_data = {}
        reactions = await cls._reaction_repository().get_my_reactions(slack_id, year, month)

        for reaction in reactions:
            if not reaction_data.get(cls.change_str_to_emoji(reaction.type)):
                reaction_data[cls.change_str_to_emoji(reaction.type)] = reaction.count
            else:
                reaction_data[cls.change_str_to_emoji(reaction.type)] += reaction.count

        return reaction_data

    @classmethod
    async def get_reaction(cls, reaction_type: str, received_user: User, send_user: User) -> ReactionMeta:
        return await cls._reaction_repository().get_current_reaction(reaction_type, received_user, send_user)

    @classmethod
    async def update_reaction(
        cls,
        reaction_type: str,
        received_user_slack_id: str,
        send_user_slack_id: str,
        is_increase: bool
    ):
        send_user = await cls._user_service.get_user(send_user_slack_id)
        received_user = await cls._user_service.get_user(received_user_slack_id)

        if send_user is None or received_user is None:
            return

        reaction = await cls.get_reaction(reaction_type, received_user, send_user)
        return await cls._reaction_repository().update_reaction(
            reaction, reaction_type, received_user, send_user, is_increase
        )

    @classmethod
    async def get_user_received_emoji_info(cls, user: User, year: int, month: int) -> UserReceivedEmojiInfo:
        reactions = await cls._reaction_repository().get_month_reactions_by_user(user, year, month)
        user_received_reactions = UserReceivedEmojiInfo(username=user.username)

        emoji_counts = {}
        for reaction in reactions:
            converted_type = cls.change_str_to_emoji(reaction.type)
            if not emoji_counts.get(converted_type):
                emoji_counts[converted_type] = ReceivedEmojiInfo(
                    type=converted_type,
                    count=reaction.count
                )
            else:
                emoji_counts[converted_type].count += reaction.count

        user_received_reactions.emoji = list(emoji_counts.values())
        return user_received_reactions

    @staticmethod
    def change_str_to_emoji(emoji_type: str) -> str:
        for best_type in settings.config.BEST_TYPES:
            if emoji_type in best_type['emoji_names']:
                return best_type['emoji']
        return '🐹'

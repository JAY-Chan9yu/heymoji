import datetime
from typing import List, Optional

from app.domains.reactions.entities import Reaction, ReceivedEmojiInfo, UserReceivedEmojiInfo, SlackEventType
from app.domains.reactions.repositories import ReactionRepository
from conf import settings
from seed_work.services import GenericService


class ReactionService(GenericService):
    _repository = ReactionRepository

    @classmethod
    async def get_monthly_reactions_by_user_id(cls, user_id: int) -> List[Reaction]:
        now = datetime.datetime.now()
        return await cls._repository().get_monthly_reactions_by_to_user_id(user_id, now.year, now.month)

    @classmethod
    async def get_by_slack_id_and_date(cls, slack_id: str, year: int, month: int) -> List[Reaction]:
        return await cls._repository().get_by_slack_id_and_date(slack_id, year, month)

    @classmethod
    async def get_by_user_id_and_date(
        cls,
        user_id: int,
        year: Optional[int] = None,
        month: Optional[int] = None
    ) -> List[Reaction]:
        return await cls._repository().get_by_user_id_and_date(user_id, year, month)

    @classmethod
    async def get_received_emoji_infos(
        cls,
        user_id: int,
        year: Optional[int] = None,
        month: Optional[int] = None
    ) -> List[UserReceivedEmojiInfo]:
        reaction_data = {}
        reactions = await cls._repository().get_by_user_id_and_date(user_id, year, month)

        for reaction in reactions:
            from_user_name = reaction.from_user.username
            reaction_emoji_info = ReceivedEmojiInfo(emoji=reaction.emoji, count=reaction.count)

            if not reaction_data.get(from_user_name):
                reaction_data[from_user_name] = UserReceivedEmojiInfo(
                    username=from_user_name,
                    emoji_infos=[reaction_emoji_info]
                )
            else:
                reaction_data[from_user_name].emoji_infos.append(reaction_emoji_info)

        return list(reaction_data.values())

    @classmethod
    async def get_reaction_by_emoji(
        cls,
        emoji: str,
        received_user_id: int,
        send_user_id: int
    ) -> Optional[Reaction]:
        """
        ??????, ?????? ?????? ID, Type ??? ???????????? Reaction ??? ????????????.
        """
        return await cls._repository().get_reaction_by_emoji(
            emoji=emoji,
            received_user_id=received_user_id,
            send_user_id=send_user_id
        )

    @classmethod
    def get_user_received_emoji_info(cls, username: str, reactions: List[Reaction]) -> UserReceivedEmojiInfo:
        """
        ????????? ?????? ?????? ????????? ????????? ???????????? ???????????? ??????
        """
        user_received_emoji_info = UserReceivedEmojiInfo(username=username)

        emoji_counts = {}
        for reaction in reactions:
            converted_emoji = cls.change_str_to_emoji(reaction.emoji)
            if not emoji_counts.get(converted_emoji):
                emoji_counts[converted_emoji] = ReceivedEmojiInfo(emoji=converted_emoji, count=reaction.count)
            else:
                emoji_counts[converted_emoji].count += reaction.count

        user_received_emoji_info.emoji_infos = list(emoji_counts.values())
        return user_received_emoji_info

    @classmethod
    async def update_or_create_reaction(
        cls,
        reaction: Reaction,
        event_type: SlackEventType,
        emoji: str,
        send_user_id: int,
        received_user_id: int
    ) -> bool:
        is_updated = True

        if reaction is None:
            if event_type == SlackEventType.ADDED_REACTION:
                now = datetime.datetime.now()
                await cls.create_reaction(
                    year=now.year,
                    month=now.month,
                    emoji=emoji,
                    to_user_id=received_user_id,
                    from_user_id=send_user_id
                )
            else:
                is_updated = False
        else:
            await cls.update_reaction_count(reaction, event_type)

        return is_updated

    @classmethod
    async def update_reaction_count(cls, reaction: Reaction, event_type: SlackEventType):
        reaction.update_count(event_type)
        await cls._repository().update(reaction)

    @classmethod
    async def create_reaction(cls, **kwargs):
        await cls._repository().insert(Reaction(**kwargs))

    @classmethod
    async def count_reaction_data(
        cls,
        slack_id: str,
        year: Optional[int] = None,
        month: Optional[int] = None
    ) -> dict:
        reaction_data = {}
        reactions = await cls._repository().get_by_slack_id_and_date(slack_id, year, month)

        for reaction in reactions:
            if not reaction_data.get(cls.change_str_to_emoji(reaction.emoji)):
                reaction_data[cls.change_str_to_emoji(reaction.emoji)] = reaction.count
            else:
                reaction_data[cls.change_str_to_emoji(reaction.emoji)] += reaction.count

        return reaction_data

    @staticmethod
    def change_str_to_emoji(emoji_type: str) -> str:
        for best_type in settings.config.ALLOWED_EMOJI_TYPES:
            if emoji_type in best_type['emoji_names']:
                return best_type['emoji']
        return '????'

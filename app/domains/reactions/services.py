import datetime
from typing import List, Optional

from app.domains.reactions.entities import Reaction, ReceivedEmojiInfo, UserReceivedEmojiInfo, SlackEventType
from app.domains.reactions.repositories import ReactionRepository
from conf import settings
from seed_work.services import GenericService


class IncreaseReactionException(Exception):
    ...


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
        """
        유저가 받은 emoji 정보를 리턴한다.
        year, month 가 없는경우 전체 emoji 정보를 가져온다.
        """
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
                emoji_idx = cls.get_emoji_infos_index_by_emoji(
                    reaction_data[from_user_name].emoji_infos,
                    reaction_emoji_info.emoji
                )
                if emoji_idx is not None:
                    reaction_data[from_user_name].emoji_infos[emoji_idx].count += reaction_emoji_info.count
                else:
                    reaction_data[from_user_name].emoji_infos.append(reaction_emoji_info)

        return list(reaction_data.values())

    @staticmethod
    def get_emoji_infos_index_by_emoji(
        emoji_infos: List[ReceivedEmojiInfo],
        emoji: str
    ) -> Optional[int]:
        """
        동일한 emoji 에 대한 정보가 리스트에 저장되어 있는지 체크한다.
        존재한다면 체크된 index를 리턴한다.
        """
        for idx, emoji_info in enumerate(emoji_infos):
            if emoji_info.emoji == emoji:
                return idx
        return None

    @classmethod
    async def get_reaction_by_emoji(
        cls,
        emoji: str,
        received_user_id: int,
        send_user_id: int
    ) -> Optional[Reaction]:
        """
        보낸, 받은 유저 ID, Type 과 일치하는 Reaction 을 반환한다.
        """
        return await cls._repository().get_reaction_by_emoji(
            emoji=emoji,
            received_user_id=received_user_id,
            send_user_id=send_user_id
        )

    @classmethod
    def get_user_received_emoji_info(cls, username: str, reactions: List[Reaction]) -> UserReceivedEmojiInfo:
        """
        유저가 받은 모든 리액션 이모지 정보들을 반환하는 함수
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
    async def add_reaction(
        cls,
        emoji: Optional[str] = None,
        send_user_id: Optional[int] = None,
        received_user_id: Optional[int] = None,
        reaction: Optional[Reaction] = None
    ):
        if all([emoji, send_user_id, received_user_id]) is False and reaction is None:
            raise IncreaseReactionException

        if reaction:
            await cls._increase_reaction_count(reaction)
        else:
            now = datetime.datetime.now()
            await cls.create_reaction(
                year=now.year,
                month=now.month,
                emoji=emoji,
                to_user_id=received_user_id,
                from_user_id=send_user_id
            )

    @classmethod
    async def remove_reaction(cls, reaction: Optional[Reaction] = None):
        await cls._decrease_reaction_count(reaction)

    @classmethod
    async def _increase_reaction_count(cls, reaction: Reaction):
        if cls.is_special_emoji(reaction.emoji):
            can_add_special_emoji = await cls._can_increase_special_emoji(reaction)
            if not can_add_special_emoji:
                return
        reaction.increase_count()
        await cls._repository().update(reaction)

    @classmethod
    async def _decrease_reaction_count(cls, reaction: Reaction):
        reaction.decrease_count()
        await cls._repository().update(reaction)

    @classmethod
    async def _can_increase_special_emoji(cls, reaction: Reaction) -> bool:
        count = await cls._repository().count_special_emoji_by_date_and_from_user(
            from_user_id=reaction.from_user_id,
            year=reaction.year,
            month=reaction.month
        )
        return count < settings.config.LIMIT_GIVE_COUNT_OF_SPECIAL_EMOJI

    @classmethod
    async def create_reaction(cls, **kwargs):
        await cls._repository().insert(Reaction(**kwargs))

    @classmethod
    async def get_reaction_count_data(
        cls,
        slack_id: str,
        year: Optional[int] = None,
        month: Optional[int] = None
    ) -> dict:
        reaction_count_data = {}
        reactions = await cls._repository().get_by_slack_id_and_date(slack_id, year, month)

        for reaction in reactions:
            if not reaction_count_data.get(cls.change_str_to_emoji(reaction.emoji)):
                reaction_count_data[cls.change_str_to_emoji(reaction.emoji)] = reaction.count
            else:
                reaction_count_data[cls.change_str_to_emoji(reaction.emoji)] += reaction.count

        return reaction_count_data

    @staticmethod
    def change_str_to_emoji(emoji_type: str) -> str:
        for best_type in settings.config.ALLOWED_EMOJI_TYPES:
            if emoji_type in best_type['emoji_names']:
                return best_type['emoji']
        return '👻'

    @staticmethod
    def is_special_emoji(emoji: str) -> bool:
        return emoji == settings.config.SPECIAL_EMOJI

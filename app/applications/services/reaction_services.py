import datetime

from app.applications.schemas import SlackEvent
from app.applications.services.user_services import UserServiceImpl
from app.domains.reactions.entities import ReactionType
from app.domains.reactions.services import ReactionService
from app.domains.users.entities import User

from conf import settings


class ReactionServiceImpl(ReactionService):
    _user_service_impl = UserServiceImpl

    @classmethod
    async def update_sending_reaction(cls, event: SlackEvent, user: User):
        """
        다른 유저가 보낸 이모지 리액션 업데이트
        """
        if event.reaction not in settings.config.REACTION_LIST:
            return

        await cls._user_service_impl.update_my_reaction(user, False)
        await cls.update_or_create_reaction_of_to_user(
            reaction_type=event.type,
            emoji=event.reaction,
            received_user_slack_id=event.item_user,
            send_user_slack_id=event.user,
        )

    @classmethod
    async def update_or_create_reaction_of_to_user(
        cls,
        reaction_type: str,
        emoji: str,
        received_user_slack_id: str,
        send_user_slack_id: str,
    ):
        send_user = await cls._user_service_impl.get_by_slack_id(send_user_slack_id)
        received_user = await cls._user_service_impl().get_by_slack_id(received_user_slack_id)

        if send_user is None or received_user is None:
            return

        reaction = await cls.get_reaction_by_type(emoji, received_user.id, send_user.id)
        if reaction is None:
            if reaction_type == ReactionType.ADDED_REACTION.value:
                now = datetime.datetime.now()
                await cls.create_reaction({
                    'year': now.year,
                    'month': now.month,
                    'emoji': emoji,
                    'to_user_id': received_user.id,
                    'from_user_id': send_user.id,
                    'count': 1
                })
        else:
            await cls.update_reaction_count(reaction, reaction_type)

    @classmethod
    async def get_this_month_best_user(cls, year: int, month: int) -> dict:
        """
        이번달 이모지 타입별 가장 많은 이모지를 받은 유저 추출
        """
        user_received_emoji_infos = []
        best_users = {}
        users = await cls._user_service_impl.get_all_users()

        for user in users:
            reactions = await cls.get_by_user_id_and_date(user.id, year, month)
            user_received_emoji_infos.append(cls.get_user_received_emoji_info(user.username, reactions))

        for best_type in settings.config.BEST_TYPES:
            max_emoji_count = 0

            for user_received_emoji_info in user_received_emoji_infos:
                try:
                    emoji_info = next(filter(
                        lambda x: x.emoji == best_type['emoji'], user_received_emoji_info.emoji_infos
                    ))

                    if max_emoji_count < emoji_info.count:
                        max_emoji_count = emoji_info.count
                        best_users[best_type['emoji']] = user_received_emoji_info.username

                except StopIteration:
                    continue

        return best_users

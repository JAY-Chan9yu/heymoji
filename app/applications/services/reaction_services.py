from typing import Optional, List

from app.applications.schemas import SlackEvent
from app.applications.services.user_services import UserAppService
from app.domains.reactions.entities import SlackEventType, UserReceivedEmojiInfo
from app.domains.reactions.services import ReactionService
from app.domains.users.entities import User

from conf import settings


class ReactionAppService:
    _reaction_domain_service = ReactionService
    _user_app_service = UserAppService

    @classmethod
    async def update_sending_reaction(cls, event: SlackEvent):
        """
        다른 유저가 보낸 이모지 리액션 업데이트
        """
        send_user = await cls._user_app_service.get_user(slack_id=event.user)
        received_user = await cls._user_app_service().get_user(slack_id=event.item_user)

        # 리액션을 send, receive 한 유저 모두 존재해야 한다
        if send_user is None or received_user is None:
            return

        await cls.update_or_create_reaction_of_received_user(
            event=event,
            send_user=send_user,
            received_user=received_user
        )

    @classmethod
    async def update_or_create_reaction_of_received_user(
        cls,
        event: SlackEvent,
        send_user: User,
        received_user: User
    ):
        """
        리액션을 받은 유저의 Reaction 을 업데이트 하거나 새로 생성
        """
        event_type = SlackEventType(event.type)
        reaction = await cls._reaction_domain_service.get_reaction_by_emoji(
            emoji=event.reaction,
            received_user_id=received_user.id,
            send_user_id=send_user.id
        )

        is_updated = await cls._reaction_domain_service.update_or_create_reaction(
            reaction=reaction,
            event_type=event_type,
            emoji=event.reaction,
            send_user_id=send_user.id,
            received_user_id=received_user.id
        )

        if is_updated:
            await cls.update_reaction_handler(send_user, event_type)

    @classmethod
    async def update_reaction_handler(cls, send_user: User, event_type: SlackEventType):
        """리액션 업데이트후 처리해야할 작업들"""
        await cls._user_app_service.update_today_assigned_reaction_count(
            is_increase=True if event_type == SlackEventType.ADDED_REACTION else False,
            user=send_user
        )

    @classmethod
    async def get_received_emoji_infos(
        cls,
        user_id: int,
        year: Optional[int] = None,
        month: Optional[int] = None
    ) -> List[UserReceivedEmojiInfo]:
        return await cls._reaction_domain_service.get_received_emoji_infos(user_id, year, month)

    @classmethod
    async def get_my_reaction_infos(
        cls,
        slack_id: str,
        year: Optional[int] = None,
        month: Optional[int] = None
    ) -> dict:
        return await cls._reaction_domain_service.count_reaction_data(slack_id, year, month)

    @classmethod
    async def get_this_month_best_users(cls, year: int, month: int) -> dict:
        """
        이번달 이모지 타입별 가장 많은 이모지를 받은 유저 추출
        """
        user_received_emoji_infos = []  # 유저가 받은 이모지 정보
        best_users = {}  # BEST_TYPES 을 통해 best 로 선정된 users

        for user in await cls._user_app_service.get_all_users():
            user_received_emoji_infos.append(cls._reaction_domain_service.get_user_received_emoji_info(
                reactions=await cls._reaction_domain_service.get_by_user_id_and_date(user.id, year, month),
                username=user.username
            ))

        for best_type in settings.config.ALLOWED_EMOJI_TYPES:
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

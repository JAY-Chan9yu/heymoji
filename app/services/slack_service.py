from enum import Enum
from typing import Union, Optional

import requests
import json

from app.domain.schemas.reaction_schema import ReactionType
from app.domain.schemas.slack_schema import SlackEventHook, SlackChallengeHook, SlackEvent
from app.domain.schemas.user_schema import User
from app.services.reaction_service import ReactionService
from app.services.user_service import UserService
from app.utils.slack_message_format import get_best_user_format, get_help_msg
from app.utils.utils import mapping_slack_command_to_dict
from conf import settings


class CommandType(Enum):
    HELP_COMMAND = 'help'
    CREATE_USER_COMMAND = 'create_user'
    UPDATE_USER_COMMAND = 'update_user'
    SHOW_THIS_MONTH_PRISE = 'show_best_member'


class SlackService:
    _user_service = UserService
    _reaction_service = ReactionService

    @classmethod
    async def slack_web_hook_handler(cls, slack_event: Union[SlackEventHook, SlackChallengeHook]) -> Optional[dict]:
        if type(slack_event) == SlackChallengeHook:
            # todo response 스키마로 만들기
            return {"challenge": slack_event.challenge}
        else:
            user = await cls._user_service.get_user(slack_event.event.user)
            await cls.slack_event_handler(event=slack_event.event, user=user)

    @classmethod
    async def slack_event_handler(cls, event: SlackEvent, user: User):

        if event.type in [ReactionType.ADDED_REACTION.value, ReactionType.REMOVED_REACTION.value]:
            if event.item_user == event.user:
                return
            await cls._reaction_service.update_reaction(event, user)
        elif event.type == ReactionType.APP_MENTION_REACTION.value:
            await cls.manage_app_mention(event)

    @classmethod
    async def manage_app_mention(cls, event: SlackEvent):
        event_command = event.text.split()
        event_command.pop(0)  # 맨션된 슬랙봇 아이디 제거
        print(f'event_command: {event_command}')

        if not event_command:
            return

        _type = event_command.pop(0).strip('--')
        mapped_attr = mapping_slack_command_to_dict(event_command)

        if _type == CommandType.HELP_COMMAND.value:
            """
            ex: <@슬랙봇> --help
            """
            cls.send_help_command()

        if _type == CommandType.CREATE_USER_COMMAND.value:
            """
            ex: <@슬랙봇> --create_user --name=JAY --slack_id=a1b1c1d1 --avatar_url=https://blablac.com/abcd
            """
            if not mapped_attr.get('slack_id'):
                return

            await cls.add_user(
                username=mapped_attr.get('name'),
                slack_id=mapped_attr.get('slack_id'),
                avatar_url=mapped_attr.get('avatar_url')
            )

        elif _type == CommandType.UPDATE_USER_COMMAND.value:
            """
            ex: <@슬랙봇> --update_user --slack_id=a1b1c1d1 --avatar_url=https://blablac.com/abcd
            """
            if not mapped_attr.get('slack_id'):
                return

            await cls.update_user(
                username=mapped_attr.get('name'),
                slack_id=mapped_attr.get('slack_id'),
                avatar_url=mapped_attr.get('avatar_url')
            )

        elif _type == CommandType.SHOW_THIS_MONTH_PRISE.value:
            """
            이번달 베스트 멤버 리스트 추출
            ex: <@슬랙봇> --show_best_member --year=12 --month=1
            """
            year = int(mapped_attr.get('year'))
            month = int(mapped_attr.get('month'))

            try:
                best_users = await cls.get_this_month_best_user(year, month)
                cls.send_best_user_list_to_slack(f"{year}년 {month}월 베스트 멤버", best_users)
            except Exception as err:
                print(err)
                return

    @classmethod
    async def add_user(cls, username: str, slack_id: str, avatar_url: str):
        user = await cls._user_service.get_user(slack_id=slack_id)
        if user:
            return

        user = User(
            username=username,
            slack_id=slack_id,
            my_reaction=settings.config.DAY_MAX_REACTION,
            avatar_url=avatar_url
        )
        await cls._user_service.create_user(user=user)

    @classmethod
    async def update_user(cls, slack_id: str, username: Optional[str], avatar_url: Optional[str]):
        user = await cls._user_service.get_user(slack_id=slack_id)
        if not user:
            return

        if username:
            user.username = username
        if avatar_url:
            user.avatar_url = avatar_url

        await cls._user_service.update_user(user=user)

    @classmethod
    async def get_this_month_best_user(cls, year: int, month: int):
        """
        이번달 이모지 타입별 가장 많은 이모지를 받은 유저 추출
        """
        user_received_emoji_infos = []
        best_users = {}
        users = await cls._user_service.get_users()

        for user in users:
            user_received_emoji_infos.append(
                await cls._reaction_service.get_user_received_emoji_info(user, year, month)
            )

        for best_type in settings.config.BEST_TYPES:
            max_emoji_count = 0

            for user_received_emoji_info in user_received_emoji_infos:
                try:
                    emoji_info = next(filter(lambda x: x.type == best_type['emoji'], user_received_emoji_info.emoji))

                    if max_emoji_count < emoji_info.count:
                        max_emoji_count = emoji_info.count
                        best_users[best_type['emoji']] = user_received_emoji_info.username

                except StopIteration:
                    continue

        return best_users

    @classmethod
    def send_help_command(cls):
        cls.send_slack_msg(get_help_msg())

    @classmethod
    def send_best_user_list_to_slack(cls, title: str, best_users: dict):
        cls.send_slack_msg(get_best_user_format(title, best_users))

    @staticmethod
    def send_slack_msg(blocks: list):
        requests.post(
            "https://slack.com/api/chat.postMessage",
            headers={"Authorization": "Bearer " + settings.config.SLACK_TOKEN, "Content-Type": "application/json"},
            data=json.dumps({"channel": settings.config.SLACK_CHANNEL, "blocks": blocks})
        )

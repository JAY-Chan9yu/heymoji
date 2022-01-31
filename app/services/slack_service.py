import asyncio
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
    HIDE_USER_COMMAND = 'hide_user'
    SHOW_USER_COMMAND = 'show_user'
    SHOW_BEST_MEMBER_COMMAND = 'show_best_member'


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
        """
        슬랙 이벤트를 받아서 type 별로 처리하는 함수
        """
        if event.type in [ReactionType.ADDED_REACTION.value, ReactionType.REMOVED_REACTION.value]:
            if event.item_user == event.user:
                return
            await cls._reaction_service.update_user_reaction(event, user)
        elif event.type == ReactionType.APP_MENTION_REACTION.value:
            await cls.mention_command_handler(event)

    @classmethod
    async def mention_command_handler(cls, event: SlackEvent):
        mention_functions = {
            CommandType.HELP_COMMAND.value: cls.send_help_command,
            CommandType.CREATE_USER_COMMAND.value: cls.add_user,
            CommandType.UPDATE_USER_COMMAND.value: cls.update_user,
            CommandType.HIDE_USER_COMMAND.value: cls.hide_user,
            CommandType.SHOW_USER_COMMAND.value: cls.show_user,
            CommandType.SHOW_BEST_MEMBER_COMMAND.value: cls.send_best_user_list_to_slack
        }
        event_command = event.text.split()
        event_command.pop(0)  # 맨션된 슬랙봇 아이디 제거

        if not event_command:
            return

        cmd = event_command.pop(0).strip('--')
        mapped_attr = mapping_slack_command_to_dict(event_command)
        func = mention_functions.get(cmd)

        if func is None:
            return

        if asyncio.iscoroutinefunction(func):
            await func(mapped_attr)
        else:
            func(mapped_attr)

    @classmethod
    async def add_user(cls, mapped_attr: dict):
        if not mapped_attr.get('slack_id'):
            return

        user = await cls._user_service.get_user(slack_id=mapped_attr['slack_id'])
        if user:
            return

        user = User(
            username=mapped_attr.get('name'),
            slack_id=mapped_attr.get('slack_id'),
            my_reaction=settings.config.DAY_MAX_REACTION,
            avatar_url=mapped_attr.get('avatar_url'),
            department=mapped_attr.get('department')
        )
        await cls._user_service.create_user(user=user)

    @classmethod
    async def update_user(cls, mapped_attr: dict):
        if not mapped_attr.get('slack_id'):
            return

        user = await cls._user_service.get_user(slack_id=mapped_attr['slack_id'])
        if not user:
            return

        if mapped_attr.get('name'):
            user.username = mapped_attr['name']
        if mapped_attr.get('avatar_url'):
            user.avatar_url = mapped_attr['avatar_url']
        if mapped_attr.get('department'):
            user.department = mapped_attr['department']

        await cls._user_service.update_user(user=user)

    @classmethod
    async def hide_user(cls, mapped_attr: dict):
        if not mapped_attr.get('slack_id'):
            return

        user = await cls._user_service.get_user(slack_id=mapped_attr.get('slack_id'))

        if not user or user.is_display is False:
            return

        user.is_display = False
        await cls._user_service.update_user(user=user)

    @classmethod
    async def show_user(cls, mapped_attr: dict):
        if not mapped_attr.get('slack_id'):
            return

        user = await cls._user_service.get_user(slack_id=mapped_attr.get('slack_id'))

        if not user or user.is_display is True:
            return

        user.is_display = True
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
    def send_help_command(cls, mapped_attr: dict):
        cls.send_slack_msg(get_help_msg())

    @classmethod
    async def send_best_user_list_to_slack(cls, mapped_attr: dict):
        year = int(mapped_attr.get('year'))
        month = int(mapped_attr.get('month'))

        try:
            best_users = await cls.get_this_month_best_user(year, month)
            cls.send_slack_msg(get_best_user_format(f"{year}년 {month}월 베스트 멤버", best_users))
        except Exception as err:
            print(err)
            return

    @staticmethod
    def send_slack_msg(blocks: list):
        requests.post(
            "https://slack.com/api/chat.postMessage",
            headers={"Authorization": "Bearer " + settings.config.SLACK_TOKEN, "Content-Type": "application/json"},
            data=json.dumps({"channel": settings.config.SLACK_CHANNEL, "blocks": blocks})
        )

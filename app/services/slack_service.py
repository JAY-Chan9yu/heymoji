import asyncio
from typing import Union, Optional, Callable

from app.domain.schemas.reaction_schema import ReactionType
from app.domain.schemas.slack_schema import SlackEventHook, SlackChallengeHook, SlackEvent, CommandType, \
    SlackMentionEvent, SlackMentionHook
from app.domain.schemas.user_schema import User
from app.services.reaction_service import ReactionService
from app.services.user_service import UserService
from app.utils.slack_message_format import get_best_user_format, get_help_msg, get_command_error_msg
from app.utils.utils import mapping_slack_command_to_dict, send_slack_msg, slack_command_exception_handler
from conf import settings


class SlackService:
    _user_service = UserService
    _reaction_service = ReactionService

    @classmethod
    async def slack_web_hook_handler(
        cls,
        slack_event: Union[SlackEventHook, SlackMentionHook, SlackChallengeHook]
    ) -> Optional[dict]:
        # 슬랙 웹훅 인증
        if type(slack_event) == SlackChallengeHook:
            return {"challenge": slack_event.challenge}
        else:
            user = await cls._user_service.get_user(slack_event.event.user)
            # 등록되지 않은 유저
            if user is None:
                return
            await cls.slack_event_handler(event=slack_event.event, user=user)

    @classmethod
    @slack_command_exception_handler()
    async def slack_event_handler(cls, event: [SlackEvent, SlackMentionEvent], user: User):
        """
        슬랙 이벤트를 받아서 type 별로 처리하는 함수
        """
        reaction = ReactionType(event.type)
        if reaction in [ReactionType.ADDED_REACTION, ReactionType.REMOVED_REACTION]:
            if event.item_user == event.user:
                return
            await cls._reaction_service.update_user_reaction(event, user)
        elif reaction == ReactionType.APP_MENTION_REACTION:
            await cls.mention_command_handler(event)

    @classmethod
    async def mention_command_handler(cls, event: SlackMentionEvent):
        mention_functions = {
            CommandType.HELP_COMMAND: cls.send_help_command,
            CommandType.CREATE_USER_COMMAND: cls.add_user,
            CommandType.UPDATE_USER_COMMAND: cls.update_user,
            CommandType.HIDE_USER_COMMAND: cls.hide_user,
            CommandType.SHOW_USER_COMMAND: cls.show_user,
            CommandType.SHOW_BEST_MEMBER_COMMAND: cls.send_best_user_list_to_slack
        }
        cmd, mapped_attr = mapping_slack_command_to_dict(event)
        func: Callable[[dict, SlackMentionEvent], None] = mention_functions.get(cmd)

        if func is None:
            send_slack_msg(channel=event.channel, blocks=get_command_error_msg())
            return

        kwargs = {'mapped_attr': mapped_attr, 'event': event}
        if asyncio.iscoroutinefunction(func):
            await func(**kwargs)
        else:
            func(**kwargs)

    @classmethod
    async def add_user(cls, **kwargs):
        mapped_attr = kwargs.get('mapped_attr')
        if not mapped_attr.get('slack_id'):
            return

        user = await cls._user_service.get_user(slack_id=mapped_attr['slack_id'])
        if user:
            return

        user = User(
            username=mapped_attr.get('name'),
            slack_id=mapped_attr.get('slack_id'),
            avatar_url=mapped_attr.get('avatar_url'),
            department=mapped_attr.get('department'),
            my_reaction=settings.config.DAY_MAX_REACTION
        )
        await cls._user_service.create_user(user=user)

    @classmethod
    async def update_user(cls, **kwargs):
        mapped_attr = kwargs.get('mapped_attr')
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
    async def hide_user(cls, **kwargs):
        mapped_attr = kwargs.get('mapped_attr')
        if not mapped_attr.get('slack_id'):
            return

        user = await cls._user_service.get_user(slack_id=mapped_attr.get('slack_id'))

        if not user or user.is_display is False:
            return

        user.is_display = False
        await cls._user_service.update_user(user=user)

    @classmethod
    async def show_user(cls, **kwargs):
        mapped_attr = kwargs.get('mapped_attr')
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
    def send_help_command(cls, **kwargs):
        event = kwargs.get('event')
        send_slack_msg(event.channel, get_help_msg())

    @classmethod
    async def send_best_user_list_to_slack(cls, **kwargs):
        mapped_attr = kwargs.get('mapped_attr')
        event = kwargs.get('event')
        year = int(mapped_attr.get('year'))
        month = int(mapped_attr.get('month'))

        try:
            best_users = await cls.get_this_month_best_user(year, month)
            send_slack_msg(event.channel, get_best_user_format(f"{year}년 {month}월 베스트 멤버", best_users))
        except Exception as err:
            print(err)
            return

import json
import logging
from typing import Callable, Any

import requests

from app.applications.schemas import SlackMentionEvent, CommandType
from app.utils.slack_message_format import get_error_msg
from conf import settings


logger = logging.getLogger(__name__)


def parsing_slack_command_to_dict(event: SlackMentionEvent) -> (CommandType, dict):
    """
    슬랙 명령어를 파싱하는 함수
    """
    mapped_attr = {'slack_id': event.user}  # reaction 한 유저의 slack_id 를 사용

    try:
        event_command = event.text.split()
        event_command.pop(0)  # 맨션된 슬랙봇 아이디 제거
        cmd = CommandType(event_command.pop(0).strip('--'))
    except (ValueError, IndexError):
        return None, mapped_attr

    for attr in event_command:
        try:
            # todo: 커맨드 형태 개선하기
            if '--avatar_url' in attr:
                info = attr.split('--avatar_url=')
                key = 'avatar_url'
                value = info[1].strip('<>')
            else:
                info = attr.split('=')
                key = info[0].replace('--', '')
                value = info[1]

            mapped_attr[key] = value
        except Exception as e:
            logger.error(f"[parsing_slack_command_to_dict] {e}")

    return cmd, mapped_attr


def send_slack_msg(channel: str, blocks: list):
    requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": f"Bearer {settings.config.SLACK_TOKEN}", "Content-Type": "application/json"},
        data=json.dumps({"channel": channel, "blocks": blocks})
    )


def slack_command_exception_handler():
    def wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
        async def _inner(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as err:
                event = kwargs.get('event')
                if not event or event.channel is None:
                    return
                send_slack_msg(channel=settings.config.ERROR_CHANNEL, blocks=get_error_msg(str(err)))
        return _inner
    return wrapper

from starlette.requests import Request

from app.applications.schemas import SlackChallengeHook, SlackMentionHook, SlackEventHook, SlackBotDirectMessageHook
from app.applications.services.slack_services import SLACK_EVENT_HOOKS
from app.domains.reactions.entities import SlackEventType


async def get_slack_event(request: Request) -> SLACK_EVENT_HOOKS:
    request = await request.json()
    if request.get('challenge'):
        return SlackChallengeHook(**request)
    elif request['event'].get('bot_profile'):
        return SlackBotDirectMessageHook(**request)
    elif request['event']['type'] in [SlackEventType.APP_MENTION_REACTION.value, SlackEventType.APP_MESSAGE.value]:
        return SlackMentionHook(**request)
    else:
        return SlackEventHook(**request)

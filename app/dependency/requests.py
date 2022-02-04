from starlette.requests import Request

from app.applications.schemas import SlackChallengeHook, SlackMentionHook, SlackEventHook
from app.domains.reactions.entities import ReactionType


async def get_slack_event(request: Request):
    request = await request.json()
    if request.get('challenge'):
        return SlackChallengeHook(**request)
    elif request['event']['type'] in [ReactionType.APP_MENTION_REACTION.value, ReactionType.APP_MESSAGE.value]:
        return SlackMentionHook(**request)
    else:
        return SlackEventHook(**request)

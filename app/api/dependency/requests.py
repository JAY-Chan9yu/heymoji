from json.decoder import JSONDecodeError
from starlette.requests import Request
from fastapi import HTTPException

from app.applications.schemas import SlackChallengeHook, SlackMentionHook, SlackEventHook, SlackBotDirectMessageHook
from app.applications.services.slack_services import SLACK_EVENT_HOOKS
from app.domains.reactions.entities import SlackEventType

async def get_slack_event(request: Request) -> SLACK_EVENT_HOOKS:
    
    request_data: dict
    try:
        request_data = await request.json()
    except JSONDecodeError:
        raise HTTPException(status_code=400, detail="request body can not be none")
    
    if request_data.get('challenge'):
        return SlackChallengeHook(**request_data)
    elif request_data['event'].get('bot_profile'):
        return SlackBotDirectMessageHook(**request_data)
    elif request_data['event']['type'] in [SlackEventType.APP_MENTION_REACTION.value, SlackEventType.APP_MESSAGE.value]:
        return SlackMentionHook(**request_data)
    else:
        return SlackEventHook(**request_data)

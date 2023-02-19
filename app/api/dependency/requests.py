from json.decoder import JSONDecodeError
from starlette.requests import Request
from fastapi import HTTPException

from app.applications.schemas import SlackChallengeHook, SlackMentionHook, SlackEventHook, SlackBotDirectMessageHook
from app.applications.services.slack_services import SLACK_EVENT_HOOKS
from app.domains.reactions.entities import SlackEventType


async def get_slack_event(request: Request) -> SLACK_EVENT_HOOKS:
    try:
        request_data: dict = await request.json()
        challenge_request = request_data.get('challenge')
        event_request = request_data.get('event')
    except JSONDecodeError:
        raise HTTPException(status_code=400, detail="request body can not be none")

    if challenge_request:
        return SlackChallengeHook(**request_data)
    elif event_request:
        if event_request.get('bot_profile'):
            return SlackBotDirectMessageHook(**request_data)
        elif is_slack_mention(event_request['type']):
            return SlackMentionHook(**request_data)
        else:
            return SlackEventHook(**request_data)
    else:
        raise HTTPException(status_code=403, detail="please check slack event")


def is_slack_mention(event_type: str) -> bool:
    return event_type in [
        SlackEventType.APP_MENTION_REACTION.value,
        SlackEventType.APP_MESSAGE.value
    ]

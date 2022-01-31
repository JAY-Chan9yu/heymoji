from fastapi import Depends, APIRouter

from app.dependency.requests import get_slack_event
from app.services.slack_service import SlackService


slack_router = APIRouter()


@slack_router.post(path="", name='슬랙 웹훅 api')
async def slack(slack_event=Depends(get_slack_event)):
    response = await SlackService.slack_web_hook_handler(slack_event)
    return response

from fastapi import Depends, APIRouter

from app.applications.services.slack_services import SlackService
from app.api.dependency.requests import get_slack_event

slack_router = APIRouter()


@slack_router.post(path="/", name='μ¬λ μΉν api')
async def slack(slack_event=Depends(get_slack_event)):
    response = await SlackService.slack_web_hook_handler(slack_event)
    return response

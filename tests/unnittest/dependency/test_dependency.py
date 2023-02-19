import pytest
from starlette.requests import Request

from app.api.dependency.requests import get_slack_event
from app.applications.schemas import SlackChallengeHook, SlackBotDirectMessageHook, SlackMentionHook, SlackEventHook


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
class TestDependencySlackHook:

    @pytest.mark.asyncio
    async def test_get_slack_event_by_challenge(self, anyio_backend, mock_challenge_request):
        dumb_request = Request(
            scope={
                "type": "http",
                "http_version": "1.1",
                "method": "POST",
                "scheme": "https",
                "client": ("127.0.0.1", 8080),
            },
        )

        event = await get_slack_event(dumb_request)
        assert isinstance(event, SlackChallengeHook)

    @pytest.mark.asyncio
    async def test_get_slack_event_by_bot_direct_message(self, anyio_backend, mock_bot_direct_message_request):
        dumb_request = Request(
            scope={
                "type": "http",
                "http_version": "1.1",
                "method": "POST",
                "scheme": "https",
                "client": ("127.0.0.1", 8080),
            },
        )

        event = await get_slack_event(dumb_request)
        assert isinstance(event, SlackBotDirectMessageHook)

    @pytest.mark.asyncio
    async def test_get_slack_event_by_slack_mention(self, anyio_backend, mock_slack_mention_request):
        dumb_request = Request(
            scope={
                "type": "http",
                "http_version": "1.1",
                "method": "POST",
                "scheme": "https",
                "client": ("127.0.0.1", 8080),
            },
        )

        event = await get_slack_event(dumb_request)
        assert isinstance(event, SlackMentionHook)

    @pytest.mark.asyncio
    async def test_get_slack_event_by_slack_event(self, anyio_backend, mock_slack_evnet_request):
        dumb_request = Request(
            scope={
                "type": "http",
                "http_version": "1.1",
                "method": "POST",
                "scheme": "https",
                "client": ("127.0.0.1", 8080),
            },
        )

        event = await get_slack_event(dumb_request)
        assert isinstance(event, SlackEventHook)
import pytest
from starlette.requests import Request

from app.api.dependency.requests import get_slack_event
from app.applications.schemas import SlackEventHook
from app.applications.services.slack_services import SlackService
from app.domains.reactions.entities import Reaction
from app.domains.reactions.repositories import ReactionRepository
from app.domains.users.repositories import UserModel
from tests.conftest import truncate_tables, test_engine
from tests.helpers.model_factories import UserModelFactory
from tests.helpers.randoms import get_random_string


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
class TestAppSlackService:
    def setup_class(self):
        self.user: UserModel = UserModelFactory(test_engine).build(**{
            "slack_id": get_random_string(20),
            "username": "test-new-slack-user",
            "avatar_url": "yoyo",
            "department": "gag-team"
        })
        self.other_user: UserModel = UserModelFactory(test_engine).build(**{
            "slack_id": get_random_string(20),
            "username": "test-new-user2",
            "avatar_url": "yoyo",
            "department": "gag-team"
        })
        self.service = SlackService

    def teardown_class(self):
        truncate_tables(["users", "reactions"])

    @pytest.mark.asyncio
    async def test_slack_web_hook_handler_by_slack_evnet_reaction_added(self, anyio_backend, mock_slack_evnet_request):
        emoji = "heart"
        reaction: Reaction = await ReactionRepository().get_reaction_by_emoji(
            emoji=emoji,
            received_user_id=self.user.id,
            send_user_id=self.other_user.id
        )
        assert reaction is None

        dumb_request = Request(
            scope={
                "type": "http",
                "http_version": "1.1",
                "method": "POST",
                "scheme": "https",
                "client": ("127.0.0.1", 8080),
            },
        )
        event_hook: SlackEventHook = await get_slack_event(dumb_request)
        event_hook.event.item_user = self.user.slack_id
        event_hook.event.user = self.other_user.slack_id
        event_hook.type = "reaction_added"
        event_hook.event.reaction = emoji
        await self.service.slack_web_hook_handler(event_hook)

        reaction: Reaction = await ReactionRepository().get_reaction_by_emoji(
            emoji=emoji,
            received_user_id=self.user.id,
            send_user_id=self.other_user.id
        )
        assert reaction is not None
        assert reaction.count == 1
        assert reaction.from_user_id == self.other_user.id
        assert reaction.to_user_id == self.user.id

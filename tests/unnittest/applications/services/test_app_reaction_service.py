from datetime import datetime
from typing import List

import pytest

from app.applications.services.reaction_services import ReactionAppService
from app.domains.reactions.entities import Reaction, UserReceivedEmojiInfo
from app.domains.reactions.repositories import ReactionRepository
from app.domains.users.repositories import UserModel
from tests.conftest import truncate_tables, test_engine
from tests.helpers.model_factories import UserModelFactory, ReactionModelFactory
from tests.helpers.randoms import get_random_string
from tests.helpers.user_creator import fake
from tests.unnittest.applications.services.conftest import get_mock_slack_evnet


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
class TestAppReactionService:
    def setup_class(self):
        self.user: UserModel = UserModelFactory(test_engine).build()
        self.other_user: UserModel = UserModelFactory(test_engine).build(**{
            "slack_id": get_random_string(20),
            "username": "test-new-user",
            "avatar_url": "yoyo",
            "department": "gag-team"
        })
        self.service = ReactionAppService

    def teardown_class(self):
        truncate_tables(["users", "reactions"])

    @pytest.mark.asyncio
    async def test_update_sending_reaction(self, db, anyio_backend):
        truncate_tables(["reactions"])
        emoji = "heart"
        slack_event = get_mock_slack_evnet(
            user_slack_id=self.other_user.slack_id,
            item_user_slack_id=self.user.slack_id,
            reaction=emoji
        )
        reaction: Reaction = await ReactionRepository().get_reaction_by_emoji(
            emoji=emoji,
            received_user_id=self.user.id,
            send_user_id=self.other_user.id
        )
        assert reaction is None

        # update reaction
        await self.service.update_sending_reaction(event=slack_event)

        reaction: Reaction = await ReactionRepository().get_reaction_by_emoji(
            emoji=emoji,
            received_user_id=self.user.id,
            send_user_id=self.other_user.id
        )
        assert reaction is not None
        assert reaction.count == 1
        assert reaction.from_user_id == self.other_user.id
        assert reaction.to_user_id == self.user.id

    @pytest.mark.asyncio
    async def test_get_received_emoji_infos(self, db, anyio_backend):
        truncate_tables(["reactions"])
        emoji = get_random_string(5)
        ReactionModelFactory(db).build(
            to_user_id=self.user.id,
            from_user_id=self.other_user.id,
            emoji=emoji
        )
        ReactionModelFactory(db).build(
            to_user_id=self.user.id,
            from_user_id=self.other_user.id,
            emoji='other-emoji'
        )
        ReactionModelFactory(db).build(
            to_user_id=self.user.id,
            from_user_id=self.other_user.id,
            emoji=emoji,
            year=1991,
            month=9
        )
        ReactionModelFactory(db).build(
            to_user_id=self.user.id,
            from_user_id=self.other_user.id,
            emoji=emoji,
            year=1991,
            month=8
        )

        user_received_emoji_infos: List[UserReceivedEmojiInfo] = await self.service.get_received_emoji_infos(
            user_id=self.user.id
        )
        assert len(user_received_emoji_infos) == 1
        assert user_received_emoji_infos[0].username == self.other_user.username
        assert user_received_emoji_infos[0].emoji_infos[0].emoji == emoji
        assert user_received_emoji_infos[0].emoji_infos[0].count == 3
        assert user_received_emoji_infos[0].emoji_infos[1].emoji == 'other-emoji'
        assert user_received_emoji_infos[0].emoji_infos[1].count == 1

        user_received_emoji_infos: List[UserReceivedEmojiInfo] = await self.service.get_received_emoji_infos(
            user_id=self.user.id,
            year=1991,
            month=9
        )
        assert len(user_received_emoji_infos) == 1
        assert user_received_emoji_infos[0].username == self.other_user.username
        assert len(user_received_emoji_infos[0].emoji_infos) == 1
        assert user_received_emoji_infos[0].emoji_infos[0].emoji == emoji
        assert user_received_emoji_infos[0].emoji_infos[0].count == 1

    @pytest.mark.asyncio
    async def test_get_my_reaction_infos(self, db, anyio_backend, mock_allowed_emoji):
        truncate_tables(["reactions"])
        for _ in range(0, 5):
            ReactionModelFactory(db).build(
                to_user_id=self.user.id,
                from_user_id=self.other_user.id,
                emoji="heart"
            )
        reaction_count_data: dict = await self.service.get_my_reaction_infos(
            slack_id=self.user.slack_id
        )
        assert reaction_count_data["❤️"] == 5

    @pytest.mark.asyncio
    async def test_get_this_month_best_users(self, db, anyio_backend, mock_allowed_emoji):
        truncate_tables(["reactions"])
        now = datetime.now()

        for emoji in ["heart", "kkkk", "pray", "+1", "eye_shaking"]:
            ReactionModelFactory(db).build(
                to_user_id=self.user.id,
                from_user_id=self.other_user.id,
                emoji=emoji
            )

        best_users: dict = await self.service.get_this_month_best_users(now.year, now.month)
        assert best_users["❤️"] == self.user.username
        assert best_users["🤣"] == self.user.username
        assert best_users["🙏️"] == self.user.username
        assert best_users["👍"] == self.user.username
        assert best_users["👀️"] == self.user.username

        for _ in range(0, 5):
            slack_event = get_mock_slack_evnet(
                user_slack_id=self.user.slack_id,
                item_user_slack_id=self.other_user.slack_id,
                reaction="heart"
            )
            await self.service.update_sending_reaction(slack_event)

        self.new_user: UserModel = UserModelFactory(test_engine).build(**{
            "slack_id": get_random_string(20),
            "username": fake.name(),
            "avatar_url": "yoyo",
            "department": "gag-team"
        })
        for _ in range(0, 5):
            slack_event = get_mock_slack_evnet(
                user_slack_id=self.user.slack_id,
                item_user_slack_id=self.new_user.slack_id,
                reaction="pray"
            )
            await self.service.update_sending_reaction(slack_event)

        best_users: dict = await self.service.get_this_month_best_users(now.year, now.month)
        assert best_users["❤️"] == self.other_user.username
        assert best_users["🤣"] == self.user.username
        assert best_users["🙏️"] == self.new_user.username
        assert best_users["👍"] == self.user.username
        assert best_users["👀️"] == self.user.username

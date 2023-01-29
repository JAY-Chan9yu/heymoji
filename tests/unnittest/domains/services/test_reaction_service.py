from datetime import datetime
from typing import List

import pytest

from app.domains.reactions.entities import Reaction, UserReceivedEmojiInfo, SlackEventType
from app.domains.reactions.services import ReactionService
from app.domains.users.repositories import UserModel
from tests.conftest import truncate_tables, test_engine
from tests.helpers.model_factories import UserModelFactory, ReactionModelFactory
from tests.helpers.randoms import get_random_string


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
class TestReactionService:
    def setup_class(self):
        self.user: UserModel = UserModelFactory(test_engine).build()
        self.other_user: UserModel = UserModelFactory(test_engine).build(**{
            "slack_id": get_random_string(20),
            "username": "test-new-user",
            "avatar_url": "yoyo",
            "department": "gag-team"
        })
        self.service = ReactionService()

    def teardown_class(self):
        truncate_tables(["users", "reactions"])

    @pytest.mark.asyncio
    async def test_get_monthly_reactions_by_user_id(self, db, anyio_backend):
        truncate_tables(["reactions"])
        now = datetime.now()
        ReactionModelFactory(db).build(
            to_user_id=self.user.id,
            from_user_id=self.other_user.id
        )
        reactions: List[Reaction] = await self.service.get_monthly_reactions_by_user_id(user_id=self.user.id)
        assert len(reactions) == 1
        assert reactions[0].year == now.year
        assert reactions[0].month == now.month
        assert reactions[0].from_user_id == self.other_user.id

    @pytest.mark.asyncio
    async def test_get_by_slack_id_and_date(self, db, anyio_backend):
        truncate_tables(["reactions"])
        now = datetime.now()
        ReactionModelFactory(db).build(
            to_user_id=self.user.id,
            from_user_id=self.other_user.id,
        )
        reactions: List[Reaction] = await self.service.get_monthly_reactions_by_user_id(
            user_id=self.user.id,
        )
        assert len(reactions) == 1
        assert reactions[0].year == now.year
        assert reactions[0].month == now.month

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
    async def test_get_reaction_by_emoji(self, db, anyio_backend):
        truncate_tables(["reactions"])
        ReactionModelFactory(db).build(
            to_user_id=self.user.id,
            from_user_id=self.other_user.id,
            emoji="test"
        )
        reaction: Reaction = await self.service.get_reaction_by_emoji(
            emoji="test",
            received_user_id=self.user.id,
            send_user_id=self.other_user.id,
        )
        assert reaction is not None
        assert reaction.count == 1
        assert reaction.from_user_id == self.other_user.id
        assert reaction.to_user_id == self.user.id

    @pytest.mark.asyncio
    async def test_get_user_received_emoji_info(self, db, anyio_backend):
        truncate_tables(["reactions"])
        for _ in range(0, 5):
            ReactionModelFactory(db).build(
                to_user_id=self.user.id,
                from_user_id=self.other_user.id,
                emoji="test"
            )
        reactions: List[Reaction] = await self.service.get_monthly_reactions_by_user_id(user_id=self.user.id)
        user_received_emoji_info: UserReceivedEmojiInfo = self.service.get_user_received_emoji_info(
            username=self.user.username,
            reactions=reactions
        )

        assert user_received_emoji_info.username == self.user.username
        assert user_received_emoji_info.emoji_infos[0].emoji == '👻'
        assert user_received_emoji_info.emoji_infos[0].count == 5

    @pytest.mark.asyncio
    async def test_update_or_create_reaction_when_reaction_is_none(self, db, anyio_backend):
        truncate_tables(["reactions"])
        is_updated = await self.service.update_or_create_reaction(
            event_type=SlackEventType.ADDED_REACTION,
            emoji="test",
            send_user_id=self.other_user.id,
            received_user_id=self.user.id,
            reaction=None
        )
        assert is_updated is True

        reaction: Reaction = await self.service.get_reaction_by_emoji(
            emoji="test",
            received_user_id=self.user.id,
            send_user_id=self.other_user.id,
        )

        assert reaction.count == 1
        assert reaction.to_user_id == self.user.id
        assert reaction.from_user_id == self.other_user.id

    @pytest.mark.asyncio
    async def test_update_or_create_reaction_when_reaction_is_not_none(self, db, anyio_backend):
        truncate_tables(["reactions"])
        ReactionModelFactory(db).build(
            to_user_id=self.user.id,
            from_user_id=self.other_user.id,
            emoji="test"
        )
        reaction: Reaction = await self.service.get_reaction_by_emoji(
            emoji="test",
            received_user_id=self.user.id,
            send_user_id=self.other_user.id,
        )

        is_updated = await self.service.update_or_create_reaction(
            event_type=SlackEventType.ADDED_REACTION,
            emoji="test",
            send_user_id=self.other_user.id,
            received_user_id=self.user.id,
            reaction=reaction
        )
        assert is_updated is True
        assert reaction.count == 2
        assert reaction.to_user_id == self.user.id
        assert reaction.from_user_id == self.other_user.id

    @pytest.mark.asyncio
    async def test_update_or_create_reaction_when_event_type_is_not_added_reaction(self, db, anyio_backend):
        truncate_tables(["reactions"])
        is_updated = await self.service.update_or_create_reaction(
            event_type=SlackEventType.REMOVED_REACTION,
            emoji="test",
            send_user_id=self.other_user.id,
            received_user_id=self.user.id,
            reaction=None
        )
        assert is_updated is False

    @pytest.mark.asyncio
    async def test_update_reaction_count_when_add_reaction(self, db, anyio_backend):
        truncate_tables(["reactions"])
        ReactionModelFactory(db).build(
            to_user_id=self.user.id,
            from_user_id=self.other_user.id,
            emoji="test"
        )
        reaction: Reaction = await self.service.get_reaction_by_emoji(
            emoji="test",
            received_user_id=self.user.id,
            send_user_id=self.other_user.id,
        )

        await self.service.update_reaction_count(
            event_type=SlackEventType.ADDED_REACTION,
            reaction=reaction
        )
        reaction: Reaction = await self.service.get_reaction_by_emoji(
            emoji="test",
            received_user_id=self.user.id,
            send_user_id=self.other_user.id,
        )
        assert reaction.count == 2

    @pytest.mark.asyncio
    async def test_update_reaction_count_when_remove_reaction(self, db, anyio_backend):
        truncate_tables(["reactions"])
        ReactionModelFactory(db).build(
            to_user_id=self.user.id,
            from_user_id=self.other_user.id,
            emoji="test"
        )
        reaction: Reaction = await self.service.get_reaction_by_emoji(
            emoji="test",
            received_user_id=self.user.id,
            send_user_id=self.other_user.id,
        )

        await self.service.update_reaction_count(
            event_type=SlackEventType.REMOVED_REACTION,
            reaction=reaction
        )
        reaction: Reaction = await self.service.get_reaction_by_emoji(
            emoji="test",
            received_user_id=self.user.id,
            send_user_id=self.other_user.id,
        )
        assert reaction.count == 0

    @pytest.mark.asyncio
    async def test_create_reaction(self, db, anyio_backend):
        truncate_tables(["reactions"])
        now = datetime.now()
        new_reaction_data = {
            "year": now.year,
            "month": now.month,
            "emoji": get_random_string(5),
            "count": 1,
            "to_user_id": self.user.id,
            "from_user_id": self.other_user.id
        }
        await self.service.create_reaction(**new_reaction_data)
        reaction: Reaction = await self.service.get_reaction_by_emoji(
            emoji=new_reaction_data["emoji"],
            received_user_id=self.user.id,
            send_user_id=self.other_user.id,
        )
        assert reaction.count == 1
        assert reaction.emoji == new_reaction_data["emoji"]
        assert reaction.to_user_id == self.user.id
        assert reaction.from_user_id == self.other_user.id

    @pytest.mark.asyncio
    async def test_get_reaction_count_data(self, db, anyio_backend, mock_allowed_emoji):
        truncate_tables(["reactions"])
        for _ in range(0, 5):
            ReactionModelFactory(db).build(
                to_user_id=self.user.id,
                from_user_id=self.other_user.id,
                emoji="heart"
            )
        reaction_count_data: dict = await self.service.get_reaction_count_data(
            slack_id=self.user.slack_id
        )
        assert reaction_count_data["❤️"] == 5

    @pytest.mark.asyncio
    async def test_change_str_to_emoji(self, db, anyio_backend, mock_allowed_emoji):
        assert self.service.change_str_to_emoji("kkkk") == "🤣"
        assert self.service.change_str_to_emoji("heart") == "❤️"
        assert self.service.change_str_to_emoji("not-exists") == '👻'

    @pytest.mark.asyncio
    async def test_is_special_emoji(self, db, anyio_backend, mock_special_emoji):
        assert self.service.is_special_emoji("👍") is True

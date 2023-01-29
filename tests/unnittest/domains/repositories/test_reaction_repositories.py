from datetime import datetime
from typing import List

import pytest

from app.domains.reactions.entities import Reaction
from app.domains.reactions.repositories import ReactionRepository, ReactionModel
from app.domains.users.repositories import UserModel
from tests.conftest import truncate_tables, test_engine
from tests.helpers.model_factories import UserModelFactory, ReactionModelFactory


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
class TestReactionRepository:
    def setup_class(self):
        self.user: UserModel = UserModelFactory(test_engine).build()
        self.other_user: UserModel = UserModelFactory(test_engine).build(**{
            "slack_id": "abcdefg",
            "username": "test-new-user",
            "avatar_url": "yoyo",
            "department": "gag-team"
        })
        self.repository = ReactionRepository()

    def teardown_class(self):
        truncate_tables(["users", "reactions"])

    @pytest.mark.asyncio
    async def test_get_by_id(self, db, anyio_backend):
        created_reaction: ReactionModel = ReactionModelFactory(db).build(
            to_user_id=self.user.id,
            from_user_id=self.other_user.id
        )
        reaction: Reaction = await self.repository.get_by_id(_id=created_reaction.id)
        assert reaction.id == created_reaction.id
        assert reaction.to_user_id == created_reaction.to_user_id
        assert reaction.from_user_id == created_reaction.from_user_id
        assert reaction.emoji == created_reaction.emoji
        assert reaction.count == created_reaction.count

    @pytest.mark.asyncio
    async def test_get_by_slack_id_and_date(self, db, anyio_backend):
        created_reaction: ReactionModel = ReactionModelFactory(db).build(
            to_user_id=self.user.id,
            from_user_id=self.other_user.id
        )
        now = datetime.now()
        reactions: List = await self.repository.get_by_slack_id_and_date(
            slack_id=self.user.slack_id,
            year=now.year,
            month=now.month
        )
        assert reactions[-1].to_user_id == created_reaction.to_user_id
        assert reactions[-1].from_user_id == created_reaction.from_user_id
        assert reactions[-1].emoji == created_reaction.emoji

    @pytest.mark.asyncio
    async def test_get_by_user_id_and_date(self, db, anyio_backend):
        created_reaction: ReactionModel = ReactionModelFactory(db).build(
            to_user_id=self.user.id,
            from_user_id=self.other_user.id
        )
        now = datetime.now()
        reactions: List = await self.repository.get_by_user_id_and_date(
            user_id=self.user.id,
            year=now.year,
            month=now.month
        )
        assert reactions[-1].to_user_id == created_reaction.to_user_id
        assert reactions[-1].from_user_id == created_reaction.from_user_id
        assert reactions[-1].emoji == created_reaction.emoji

    @pytest.mark.asyncio
    async def test_get_reaction_by_emoji(self, db, anyio_backend):
        created_reaction: ReactionModel = ReactionModelFactory(db).build(
            to_user_id=self.user.id,
            from_user_id=self.other_user.id,
            emoji="pray"
        )
        reaction: Reaction = await self.repository.get_reaction_by_emoji(
            emoji="pray",
            received_user_id=self.user.id,
            send_user_id=self.other_user.id
        )
        assert reaction.to_user_id == created_reaction.to_user_id
        assert reaction.from_user_id == created_reaction.from_user_id
        assert reaction.emoji == "pray"
        assert reaction.emoji == created_reaction.emoji

    @pytest.mark.asyncio
    async def test_insert(self, db, anyio_backend):
        now = datetime.now()
        new_reaction = Reaction(
            year=now.year,
            month=now.month,
            emoji="insert",
            count=100,
            to_user_id=self.user.id,
            from_user_id=self.other_user.id
        )
        await self.repository.insert(new_reaction)
        reaction: Reaction = await self.repository.get_reaction_by_emoji(
            emoji="insert",
            received_user_id=self.user.id,
            send_user_id=self.other_user.id
        )
        assert reaction.to_user_id == new_reaction.to_user_id
        assert reaction.from_user_id == new_reaction.from_user_id
        assert reaction.emoji == "insert"
        assert reaction.emoji == new_reaction.emoji
        assert reaction.count == 100

    @pytest.mark.asyncio
    async def test_update(self, db, anyio_backend):
        ReactionModelFactory(db).build(
            to_user_id=self.user.id,
            from_user_id=self.other_user.id,
            emoji="update-test"
        )
        before_reaction: Reaction = await self.repository.get_reaction_by_emoji(
            emoji="update-test",
            received_user_id=self.user.id,
            send_user_id=self.other_user.id
        )
        assert before_reaction.count == 1

        before_reaction.count = 100

        await self.repository.update(before_reaction)
        reaction: Reaction = await self.repository.get_reaction_by_emoji(
            emoji="update-test",
            received_user_id=self.user.id,
            send_user_id=self.other_user.id
        )
        assert reaction.emoji == before_reaction.emoji
        assert reaction.count == 100

    @pytest.mark.asyncio
    async def test_get_monthly_reactions_by_to_user_id(self, db, anyio_backend):
        truncate_tables(["reactions"])
        now = datetime.now()
        total_reaction_cnt = 5

        for i in range(0, total_reaction_cnt):
            ReactionModelFactory(db).build(
                to_user_id=self.user.id,
                from_user_id=self.other_user.id,
                emoji=f"emoji-{i}"
            )

        reactions: List = await self.repository.get_monthly_reactions_by_to_user_id(
            to_user_id=self.user.id,
            month=now.month,
            year=now.year
        )
        assert len(reactions) == total_reaction_cnt
        for i, reaction in enumerate(reactions):
            assert reaction.emoji == f"emoji-{i}"

    @pytest.mark.asyncio
    async def test_count_given_special_emoji_by_date_and_user(self, db, anyio_backend):
        truncate_tables(["reactions"])
        now = datetime.now()
        total_reaction_cnt = 5

        for i in range(0, total_reaction_cnt):
            ReactionModelFactory(db).build(
                to_user_id=self.user.id,
                from_user_id=self.other_user.id,
                emoji=f"emoji-{i}"
            )

        reactions: List = await self.repository.get_monthly_reactions_by_to_user_id(
            to_user_id=self.user.id,
            month=now.month,
            year=now.year
        )
        assert len(reactions) == total_reaction_cnt
        for i, reaction in enumerate(reactions):
            assert reaction.emoji == f"emoji-{i}"

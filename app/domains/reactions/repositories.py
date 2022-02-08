from datetime import datetime
from typing import List, Optional

from sqlalchemy import select, update, insert, Column, Integer, ForeignKey, String
from sqlalchemy.orm import joinedload, relationship

from app.Infrastructure.database import async_session_manager, Base
from app.domains.reactions.entities import Reaction
from app.domains.users.repositories import UserModel
from seed_work.repositories import GenericRepository


class ReactionModel(Base):
    __tablename__ = 'reactions'

    id = Column(Integer, primary_key=True, index=True)
    to_user_id = Column(Integer, ForeignKey("users.id"))
    from_user_id = Column(Integer, ForeignKey("users.id"))
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    emoji = Column(String(50), nullable=True)
    count = Column(Integer, default=0)

    to_user = relationship(UserModel, foreign_keys=[to_user_id])
    from_user = relationship(UserModel, foreign_keys=[from_user_id])


class ReactionRepository(GenericRepository):
    model = ReactionModel

    async def get_by_id(self, _id: int) -> Optional[Reaction]:
        q = select(self.model).filter(self.model.id == _id)
        async with async_session_manager() as session:
            results = await session.execute(q)
            for result in results:
                return Reaction(**result[0].__dict__)

    async def get_by_slack_id_and_date(self, slack_id: str, year: int, month: int) -> List[Reaction]:
        q = select(self.model).options(
            joinedload(self.model.from_user),
            joinedload(self.model.to_user),
        ).filter(
            self.model.to_user.has(slack_id=slack_id),
        )

        if year:
            q = q.filter(self.model.year == year)
        if month:
            q = q.filter(self.model.month == month)

        reactions = []
        async with async_session_manager() as session:
            results = await session.execute(q)
            for result in results:
                reactions.append(Reaction(**result[0].__dict__))

        return reactions

    async def get_by_user_id_and_date(self, user_id: int, year: int, month: int) -> List[Reaction]:
        q = select(
            self.model
        ).options(
            joinedload(self.model.from_user),
            joinedload(self.model.to_user),
        ).filter(
            self.model.to_user_id == user_id
        )

        if year:
            q = q.filter(self.model.year == year)
        if month:
            q = q.filter(self.model.month == month)

        reactions = []
        async with async_session_manager() as session:
            results = await session.execute(q)
            for result in results:
                reactions.append(Reaction(**result[0].__dict__))

        return reactions

    async def get_reaction_by_emoji(
        self,
        emoji: str,
        received_user_id: int,
        send_user_id: int
    ) -> Optional[Reaction]:
        now_date = datetime.now().date()

        q = select(
            self.model
        ).filter(
            self.model.year == now_date.year,
            self.model.month == now_date.month,
            self.model.from_user_id == send_user_id,
            self.model.to_user_id == received_user_id,
            self.model.emoji == emoji
        )

        async with async_session_manager() as session:
            results = await session.execute(q)
            for result in results:
                return Reaction(**result[0].__dict__)

    async def insert(self, reaction: Reaction):
        q = insert(self.model).values(reaction.entity_to_data())
        async with async_session_manager() as session:
            await session.execute(q)

    async def update(self, reaction: Reaction):
        q = update(self.model).filter(self.model.id == reaction.id).values(reaction.entity_to_data())
        async with async_session_manager() as session:
            await session.execute(q)

    async def get_monthly_reactions_by_to_user_id(self, to_user_id: int, year: int, month: int) -> List[Reaction]:
        reactions = []

        q = select(
            self.model
        ).filter(
            self.model.year == year,
            self.model.month == month,
            self.model.to_user_id == to_user_id
        )

        async with async_session_manager() as session:
            results = await session.execute(q)
            for result in results:
                reactions.append(Reaction(**result[0].__dict__))

        return reactions

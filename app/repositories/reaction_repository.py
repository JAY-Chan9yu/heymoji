from datetime import datetime
from typing import List

from sqlalchemy import select, update, insert
from sqlalchemy.orm import joinedload

from app.domain.models.reaction_model import ReactionModel
from app.domain.schemas.reaction_schema import ReceivedEmojiInfo, Reaction, UserReceivedEmojiInfo, ReactionMeta
from app.domain.schemas.user_schema import User
from app.repositories.base_repository import BaseRepository


class ReactionRepository(BaseRepository):

    def __init__(self, is_async: bool = True):
        self.session = self.get_connection(is_async)

    async def get_my_reactions(self, slack_id: str, year: int, month: int) -> list:
        q = select(ReactionModel).options(
            joinedload(ReactionModel.from_user),
            joinedload(ReactionModel.to_user),
        ).filter(
            ReactionModel.to_user.has(slack_id=slack_id),
        )
    
        if year:
            q = q.filter(ReactionModel.year == year)
        if month:
            q = q.filter(ReactionModel.month == month)
    
        reactions = []
        for reaction_column in await self.session.execute(q):
            reactions.append(ReactionMeta(**reaction_column[0].__dict__))
        return reactions

    async def get_reactions(self, user_id: int, year: int, month: int) -> List:
        reaction_data = {}

        q = select(
            ReactionModel
        ).options(
            joinedload(ReactionModel.from_user),
            joinedload(ReactionModel.to_user),
        ).filter(
            ReactionModel.to_user_id == user_id
        )

        if year:
            q = q.filter(ReactionModel.year == year)
        if month:
            q = q.filter(ReactionModel.month == month)

        for reaction_column in await self.session.execute(q):
            reaction = Reaction(**reaction_column[0].__dict__)
            from_user_name = reaction.from_user.username

            if not reaction_data.get(from_user_name):
                reaction_data[from_user_name] = UserReceivedEmojiInfo(
                    username=from_user_name,
                    emoji=[ReceivedEmojiInfo(type=reaction.type, count=reaction.count)]
                )
            else:
                reaction_data[from_user_name].emoji.append(
                    ReceivedEmojiInfo(type=reaction.type, count=reaction.count)
                )

        return list(reaction_data.values())

    async def get_current_reaction(self, reaction_type: str, received_user: User, send_user: User) -> ReactionMeta:
        now_date = datetime.now().date()

        results = await self.session.execute(
            select(
                ReactionModel
            ).filter(
                ReactionModel.year == now_date.year,
                ReactionModel.month == now_date.month,
                ReactionModel.from_user_id == send_user.id,
                ReactionModel.to_user_id == received_user.id,
                ReactionModel.type == reaction_type
            )
        )

        for result in results:
            return ReactionMeta(**result[0].__dict__)

    async def get_month_reactions_by_user(self, user: User, year: int, month: int) -> List[ReactionMeta]:
        reactions = []
        results = await self.session.execute(
            select(
                ReactionModel
            ).filter(
                ReactionModel.year == year,
                ReactionModel.month == month,
                ReactionModel.to_user_id == user.id
            )
        )

        for result in results:
            reactions.append(ReactionMeta(**result[0].__dict__))
        return reactions

    async def update_added_reaction(
        self,
        reaction: ReactionMeta,
        reaction_type: str,
        received_user: User,
        send_user: User,
        is_increase: bool
    ):
        now_date = datetime.now()

        if is_increase and reaction is None:
            reaction = ReactionMeta(
                year=now_date.year,
                month=now_date.month,
                type=reaction_type,
                from_user_id=send_user.id,
                to_user_id=received_user.id,
                count=1
            )
            await self.session.execute(insert(ReactionModel).values(reaction.__dict__))
            await self.session.commit()

        elif reaction:
            if is_increase is False and reaction.count == 0:
                return
            reaction.count += 1 if is_increase else -1
            await self.session.execute(
                update(ReactionModel).filter(
                    ReactionModel.id == reaction.id
                ).values(
                    {'count': reaction.count}
                )
            )
            await self.session.commit()

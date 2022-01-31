from typing import Optional

from sqlalchemy import func, and_, desc, select, insert, update

from app.domain.models.reaction_model import ReactionModel
from app.domain.models.user_model import UserModel
from app.domain.schemas.user_schema import User, UserDetailInfo
from app.repositories.base_repository import BaseRepository, async_session_manager


class UserRepository(BaseRepository):

    async def get_user(self, slack_id: str) -> Optional[User]:
        q = select(UserModel).filter(UserModel.slack_id == slack_id)
        async with async_session_manager() as session:
            results = await session.execute(q)
            for result in results:
                return User(**result[0].__dict__)

    async def get_users(self):
        users = []
        q = select(UserModel)

        async with async_session_manager() as session:
            results = await session.execute(q)
            for result in results:
                users.append(User(**result[0].__dict__))

        return users

    async def get_detail_user(
        self,
        year: Optional[int] = None,
        month: Optional[int] = None,
        department: Optional[str] = None
    ):
        user_infos = []
        sub = select(ReactionModel.to_user_id, func.sum(ReactionModel.count)).group_by(ReactionModel.to_user_id)

        if year and month:
            sub = sub.filter(ReactionModel.year == year, ReactionModel.month == month)
        elif year:
            sub = sub.filter(ReactionModel.year == year)
        elif month:
            sub = sub.filter(ReactionModel.month == month)

        sub = sub.subquery()

        q = select(
            UserModel.id,
            UserModel.avatar_url,
            UserModel.username,
            UserModel.department,
            UserModel.my_reaction,
            func.ifnull(sub.c.get('sum(reactions.count)'), 0).label('received_reaction_count')
        ).filter(
            UserModel.is_display == 1
        ).outerjoin(
            sub, and_(sub.c.to_user_id == UserModel.id)
        ).order_by(
            desc('received_reaction_count')
        )

        if department:
            q = q.filter(UserModel.department == department)

        async with async_session_manager() as session:
            results = await session.execute(q)
            for result in results:
                user_infos.append(UserDetailInfo(**result._asdict()))

        return user_infos

    async def create_user(self, user: User) -> User:
        q = insert(UserModel).values(user.__dict__)
        async with async_session_manager() as session:
            await session.execute(q)
        return user

    async def update_user(self, user: User):
        q = update(UserModel).filter(UserModel.id == user.id).values(user.__dict__)
        async with async_session_manager() as session:
            await session.execute(q)

    async def update_my_reaction(self, user: User, is_increase: bool):
        """내가 가지고 있는 reaction count 업데이트"""
        user.my_reaction += 1 if is_increase else -1
        q = update(UserModel).filter(UserModel.id == user.id).values({'my_reaction': user.my_reaction})
        async with async_session_manager() as session:
            await session.execute(q)

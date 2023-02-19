from typing import Optional, List

from sqlalchemy import func, and_, desc, select, insert, update, Column, Integer, String, Boolean

from app.Infrastructure.database import async_session_manager, Base
from app.domains.users.entities import User, UserDetailInfo
from seed_work.repositories import GenericRepository


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    slack_id = Column(String(50), nullable=False, unique=True)
    username = Column(String(100), nullable=False)
    avatar_url = Column(String(500), nullable=True)
    department = Column(String(50), nullable=True)
    is_display = Column(Boolean, default=True)


class UserRepository(GenericRepository):
    model = UserModel

    async def get_by_id(self, _id: int) -> Optional[User]:
        q = select(self.model).filter(self.model.id == _id)
        async with async_session_manager() as session:
            results = await session.execute(q)
            for result in results:
                return User(**result[0].__dict__)
        return None

    async def get_by_slack_id(self, slack_id: str) -> Optional[User]:
        q = select(self.model).filter(self.model.slack_id == slack_id)
        async with async_session_manager() as session:
            results = await session.execute(q)
            for result in results:
                return User(**result[0].__dict__)
        return None

    async def get_all_users(self) -> List[User]:
        # todo: pagination 추가하기
        users = []
        q = select(self.model)
        async with async_session_manager() as session:
            results = await session.execute(q)
            for result in results:
                users.append(User(**result[0].__dict__))
        return users

    async def insert(self, user: User) -> User:
        q = insert(self.model).values(user.entity_to_data())
        async with async_session_manager() as session:
            await session.execute(q)
        return user

    async def update(self, user: User):
        q = update(
            self.model
        ).filter(
            self.model.id == user.id
        ).values(
            user.entity_to_data()
        )
        async with async_session_manager() as session:
            await session.execute(q)

    async def get_detail_info(self, **kwargs) -> List[UserDetailInfo]:
        """
        유저가 받은 리액션 상세 정보 엔티티를 반환
        """
        from app.domains.reactions.repositories import ReactionModel

        user_infos = []
        year = kwargs.get('year')
        month = kwargs.get('month')
        department = kwargs.get('department')

        # Reaction Sub Query
        sub = select(
            ReactionModel.to_user_id,
            func.sum(ReactionModel.count)
        ).group_by(
            ReactionModel.to_user_id
        )

        if year and month:
            sub = sub.filter(ReactionModel.year == year, ReactionModel.month == month)
        elif year:
            sub = sub.filter(ReactionModel.year == year)
        elif month:
            sub = sub.filter(ReactionModel.month == month)

        sub = sub.subquery()

        q = select(
            self.model.id,
            self.model.avatar_url,
            self.model.username,
            self.model.department,
            self.model.is_display,
            func.ifnull(sub.c.get('sum(reactions.count)'), 0).label('received_reaction_count')
        ).filter(
            self.model.is_display == 1
        ).outerjoin(
            sub, and_(sub.c.to_user_id == self.model.id)
        ).order_by(
            desc('received_reaction_count')
        )

        if department:
            q = q.filter(self.model.department == department)

        async with async_session_manager() as session:
            results = await session.execute(q)
            for result in results:
                user_infos.append(UserDetailInfo(**result._asdict()))

        return user_infos

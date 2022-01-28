from sqlalchemy import func, and_, desc
from sqlalchemy.orm import Session

from app.domain.models.reaction_model import ReactionModel
from app.domain.models.user_model import UserModel
from app.domain.schemas.user_schema import User, UserDetailInfo
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):

    def __init__(self):
        self.session: Session = self.get_connection()

    def get_user(self, slack_id: str) -> User:
        user_model = self.session.query(UserModel).filter(UserModel.slack_id == slack_id).first()
        return User(**user_model.__dict__)

    def get_users(self, year: int, month: int):
        """
        :param year: 년
        :param month: 월
        """
        sub = self.session.query(ReactionModel.to_user_id, func.sum(ReactionModel.count))

        if year and month:
            sub = sub.filter(ReactionModel.year == year, ReactionModel.month == month)
        elif year:
            sub = sub.filter(ReactionModel.year == year)
        elif month:
            sub = sub.filter(ReactionModel.month == month)
        sub = sub.group_by(ReactionModel.to_user_id).subquery()

        users = self.session.query(
            UserModel.id,
            UserModel.avatar_url,
            UserModel.username,
            UserModel.my_reaction,
            func.ifnull(sub.c.get('sum(reactions.count)'), 0).label('received_reaction_count')
        ).outerjoin(
            sub, and_(sub.c.to_user_id == UserModel.id)
        ).order_by(
            desc('received_reaction_count')
        ).all()

        user_infos = []
        for user in users:
            user_infos.append(
                UserDetailInfo(
                    id=user.id,
                    avatar_url=user.avatar_url,
                    username=user.username,
                    my_reaction=user.my_reaction,
                    received_reaction_count=user.received_reaction_count
                )
            )

        return user_infos

    def create_user(self, user: User):
        db_user = UserModel(slack_id=user.slack_id, username=user.username, avatar_url=user.avatar_url)
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)

        return db_user

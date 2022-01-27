from sqlalchemy import func, and_, desc
from sqlalchemy.orm import Session

from app import schemas
from app.models.reaction_model import Reaction
from app.models.user_model import User
from app.repositories.base_repository import BaseRepository

from app.schemas import ReceivedReactionUser


class UserRepository(BaseRepository):

    def __init__(self):
        self.session: Session = self.get_connection()

    def get_user(self, slack_id: str):
        return self.session.query(User).filter(User.slack_id == slack_id).first()

    def get_users(self, year: int, month: int):
        """
        :param year: 년
        :param month: 월
        """
        sub = self.session.query(Reaction.to_user_id, func.sum(Reaction.count))

        if year and month:
            sub = sub.filter(Reaction.year == year, Reaction.month == month)
        elif year:
            sub = sub.filter(Reaction.year == year)
        elif month:
            sub = sub.filter(Reaction.month == month)
        sub = sub.group_by(Reaction.to_user_id).subquery()

        users = self.session.query(
            User.id,
            User.avatar_url,
            User.username,
            User.my_reaction,
            func.ifnull(sub.c.get('sum(reactions.count)'), 0).label('received_reaction')
        ).outerjoin(
            sub, and_(sub.c.to_user_id == User.id)
        ).order_by(
            desc('received_reaction')
        ).all()

        user_infos = []
        for user in users:
            user_infos.append(
                ReceivedReactionUser(
                    id=user.id,
                    avatar_url=user.avatar_url,
                    username=user.username,
                    my_reaction=user.my_reaction,
                    received_reaction=user.received_reaction
                )
            )

        return user_infos

    def create_user(self, user: schemas.UserCreate):
        db_user = User(slack_id=user.slack_id, username=user.username, avatar_url=user.avatar_url)
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)

        return db_user

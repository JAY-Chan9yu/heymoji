from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.user_model import User
from app.repositories.base_repository import Base


class Reaction(Base):
    __tablename__ = "reactions"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    to_user_id = Column(Integer, ForeignKey("users.id"))  # 리액션을 받은 유저
    from_user_id = Column(Integer, ForeignKey("users.id"))  # 리액션을 보낸 유저
    to_user = relationship(User, foreign_keys=[to_user_id])
    from_user = relationship(User, foreign_keys=[from_user_id])

    type = Column(String(50), nullable=True)  # 리액션 타입 (이모지 종류)
    count = Column(Integer, default=0)  # 받은 개수

from sqlalchemy import Column, Integer, String

from app.repositories.base_repository import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=True)  # display name
    slack_id = Column(String(50), nullable=False, unique=True)
    my_reaction = Column(Integer, nullable=False, default=5)  # 사용할 수 있는 리액션(이모지) 개수
    avatar_url = Column(String(500), nullable=True)  # 프로필 이미지 url

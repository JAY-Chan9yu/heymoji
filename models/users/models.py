from sqlalchemy import Column, Integer, String, Float, Boolean

from conf import database


class User(database.Base):
    __tablename__ = "slack_user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=True) # display name
    slack_id = Column(String(50), nullable=False) # 슬랙 아이디
    get_emoji_count = Column(Integer, nullable=False, default=0) # 받은 이모지 개수
    using_emoji_count = Column(Integer, nullable=False, default=0) # 사용할 수 있는 이모지 개수
    avatar_url = Column(String(100), nullable=True)  # 프로필 이미지 url

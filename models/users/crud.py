from sqlalchemy.orm import Session

from models.users import models, schemas
from models.users.models import User


def get_user(db: Session, item_user: str):
    return db.query(models.User).filter(models.User.slack_id == item_user).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(slack_id=user.slack_id, username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def update_get_emoji(db: Session, slack_id: str, is_increase: bool):
    db_user = db.query(models.User).filter(models.User.slack_id == slack_id).one_or_none()
    if db_user is None:
        return None

    if is_increase:
        db_user.get_emoji_count += 1
    else:
        db_user.get_emoji_count -= 1

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def update_using_emoji_count(db: Session, user: User, is_increase: bool):
    if is_increase:
        user.using_emoji_count += 1
    else:
        user.using_emoji_count -= 1

    db.add(user)
    db.commit()
    db.refresh(user)

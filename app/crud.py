from datetime import datetime

from sqlalchemy import text, literal_column
from sqlalchemy.orm import Session

from app import schemas
from app.models import User, Reaction


def get_user(db: Session, item_user: str):
    return db.query(User).filter(User.slack_id == item_user).first()


def get_users(db: Session, year: int, month: int):
    """
    :param db:
    :param year: 년
    :param month: 월
    """

    # TODO: sqlalchemy ORM이 익숙하지 않아 raw Query 사용 -> ORM으로 변환해보기
    _filter = ''
    if year and month:
        _filter = f'where month={year} AND month={month}'
    elif year:
        _filter = f'where year={year}'
    elif year:
        _filter = f'where month={month}'

    return db.query(
        literal_column("avatar_url"),
        literal_column("username"),
        literal_column("my_reaction"),
        literal_column("received_reaction")
    ).from_statement(text(
        "select avatar_url, username, my_reaction, IFNULL(re.count, 0) as received_reaction "
        "from users left outer join ("
        f"select to_user, sum(count) as count from reactions {_filter} group by to_user) "
        "as re on re.to_user = users.id order by received_reaction desc")
    ).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = User(slack_id=user.slack_id, username=user.username, avatar_url=user.avatar_url)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def update_added_reaction(db: Session, type: str, item_user: str, user: str, is_increase: bool):
    """
    :param item_user: 리액션을 받는 유저
    :param type: 리액션 타입(이모지 종류)
    :param user: 리액션을 한 유저
    :param is_increase: count 증가/감소
    """
    # ex: session.query(MyUserClass).filter(MyUserClass.id.in_((123,456))).all()
    from_user = db.query(User).filter(User.slack_id == item_user).one_or_none()
    to_user = db.query(User).filter(User.slack_id == user).one_or_none()

    if to_user is None or from_user is None:
        return

    now_date = datetime.now().date()
    reaction = db.query(Reaction).filter(
        Reaction.year == now_date.year, Reaction.month == now_date.month,
        Reaction.from_user == from_user.id, Reaction.to_user == to_user.id
    ).first()

    # 1. 리액션이 있는경우
    # 2  리액션이 없는데 감소 해야하는 경우 return
    # 3. 리액션이 없는데 증가해야하는 경우
    if reaction:
        if is_increase is False and reaction.count == 0:
            return
        reaction.count += 1 if is_increase else -1
    elif is_increase:
        reaction = Reaction(
            year=now_date.year, month=now_date.month, type=type, from_user=from_user.id, to_user=to_user.id)
        reaction.count = 1
    else:
        return

    db.add(reaction)
    db.commit()
    db.refresh(reaction)


def check_reaction(db: Session, user: User, is_increase: bool):
    if is_increase:
        user.my_reaction += 1
    else:
        user.my_reaction -= 1

    db.add(user)
    db.commit()
    db.refresh(user)

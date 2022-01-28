from datetime import datetime

from sqlalchemy.orm import Session, joinedload

from app.domain.models.reaction_model import ReactionModel
from app.domain.models.user_model import UserModel
from app.domain.schemas.reaction_schema import ReceivedEmojiInfo
from app.domain.schemas.user_schema import UserReceivedReactions, User
from app.repositories.base_repository import BaseRepository


BEST_LOVE = ['heart']
BEST_FUNNY = ['kkkk', '기쁨']
BEST_HELP = ['pray', '기도']
BEST_GOOD = ['+1', 'wow', 'wonderfulk', '천재_개발자']
BEST_BAD = ['eye_shaking']


class ReactionRepository(BaseRepository):

    def __init__(self):
        self.session: Session = self.get_connection()

    def get_my_reaction(self, slack_id: str, year: int, month: int):
    
        reactions = self.session.query(ReactionModel).options(
            joinedload(ReactionModel.from_user),
            joinedload(ReactionModel.to_user),
        ).filter(
            ReactionModel.to_user.has(slack_id=slack_id),
        )
    
        if year:
            reactions = reactions.filter(ReactionModel.year == year)
        if month:
            reactions = reactions.filter(ReactionModel.month == month)
    
        def change_str_to_emoji(emoji_type: str):
            if emoji_type in BEST_LOVE:
                return '❤️'
            elif emoji_type in BEST_FUNNY:
                return '🤣'
            elif emoji_type in BEST_HELP:
                return '🙏'
            elif emoji_type in BEST_GOOD:
                return '👍'
            elif emoji_type in BEST_BAD:
                return '👀'
            else:
                return '🐹'
    
        reaction_data = {}
        for reaction in reactions:
            if not reaction_data.get(change_str_to_emoji(reaction.type)):
                reaction_data[change_str_to_emoji(reaction.type)] = reaction.count
            else:
                reaction_data[change_str_to_emoji(reaction.type)] += reaction.count
    
        return reaction_data
    
    def get_reactions(self, user_id: int, year: int, month: int):
        reactions = self.session.query(ReactionModel).options(
            joinedload(ReactionModel.from_user),
            joinedload(ReactionModel.to_user),
        ).filter(
            ReactionModel.to_user_id == user_id,
        )
    
        if year:
            reactions = reactions.filter(ReactionModel.year == year)
        if month:
            reactions = reactions.filter(ReactionModel.month == month)
    
        reaction_data = {}
        for reaction in reactions:
            from_user_name = reaction.from_user.username
            if not reaction_data.get(from_user_name):
                reaction_data[from_user_name] = {
                    'emoji_infos': [ReceivedEmojiInfo(type=reaction.type, count=reaction.count)]
                }
            else:
                reaction_data[from_user_name]['emoji_infos'].append(
                    ReceivedEmojiInfo(type=reaction.type, count=reaction.count)
                )
    
        return [UserReceivedReactions(username=key, emoji=value.get('emoji_infos')) for key, value in reaction_data.items()]
    
    def update_added_reaction(self, type: str, item_user: str, user: str, is_increase: bool):
        """
        :param item_user: 리액션을 받는 유저 -> to_user
        :param type: 리액션 타입(이모지 종류) -> from_user
        :param user: 리액션을 한 유저
        :param is_increase: True: Added, False: Removed
        """
        from_user = self.session.query(UserModel).filter(UserModel.slack_id == user).one_or_none()
        to_user = self.session.query(UserModel).filter(UserModel.slack_id == item_user).one_or_none()
    
        if to_user is None or from_user is None:
            return
    
        now_date = datetime.now().date()
        reaction = self.session.query(ReactionModel).filter(
            ReactionModel.year == now_date.year, ReactionModel.month == now_date.month,
            ReactionModel.from_user_id == from_user.id, ReactionModel.to_user_id == to_user.id,
            ReactionModel.type == type
        ).first()
    
        """
        1. 리액션이 있는경우 (remove 인 경우 받은 reaction이 0개 인 경우 return)
        2  리액션이 없는데 감소 해야하는 경우 return
        3. 리액션이 없는데 증가해야하는 경우
        """
        if reaction:
            if is_increase is False and reaction.count == 0:
                return
            reaction.count += 1 if is_increase else -1
        elif is_increase:
            reaction = ReactionModel(
                year=now_date.year,
                month=now_date.month,
                type=type,
                from_user_id=from_user.id,
                to_user_id=to_user.id
            )
            reaction.count = 1
        else:
            return
    
        self.session.add(reaction)
        self.session.commit()
        self.session.refresh(reaction)
    
    def update_my_reaction(self, user: User, is_increase: bool):
        """
        내가 가지고 있는 reaction count 업데이트
        :param is_increase: True: Added, False: Removed
        """
        user.my_reaction += 1 if is_increase else -1
    
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
    
    def get_member_reaction_count(self, user: User, year: int, month: int):
        """
        멤버가 받은 reaction을 현재 prise type별로 가지고 오는 함수
        {user_id : '123123', love : 3, funny : 5, help : 5, good : 10, bad : 5}
        """
    
        # 리액션별로 count
        reaction_list = self.session.query(ReactionModel).filter(
            ReactionModel.to_user_id == user.id,
            ReactionModel.year == year,
            ReactionModel.month == month
        )
    
        result = {
            'username': user.username,
            'love': 0,
            'funny': 0,
            'help': 0,
            'good': 0,
            'bad': 0,
        }
    
        for reaction in reaction_list:
            if reaction.type in BEST_LOVE:
                result['love'] += 1
            elif reaction.type in BEST_FUNNY:
                result['funny'] += 1
            elif reaction.type in BEST_HELP:
                result['help'] += 1
            elif reaction.type in BEST_GOOD:
                result['help'] += 1
            elif reaction.type in BEST_BAD:
                result['bad'] += 1
    
        return result

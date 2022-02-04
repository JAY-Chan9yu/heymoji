from typing import Optional

from pydantic import Field

from conf import settings
from seed_work.entities import AggregateRoot, Entity


class User(AggregateRoot):
    slack_id: str
    username: str = Field(title='유저네임')
    avatar_url: Optional[str] = Field(title='아바타 URL', default=None)
    department: Optional[str] = Field(title='부서', default=None)
    is_display: bool = Field(title='노출여부', default=True)
    my_reaction: int = Field(title='하루에 줄 수 있는 리액션 카운트', default=settings.config.DAY_MAX_REACTION)

    def show_user(self):
        if self.is_display is False:
            self.is_display = True

    def hide_user(self):
        if self.is_display is True:
            self.is_display = False

    def decrease_my_reaction(self):
        if self.my_reaction > 0:
            self.my_reaction -= 1

    def increase_my_reaction(self):
        if self.my_reaction < settings.config.DAY_MAX_REACTION:
            self.my_reaction += 1

    def update_attr(self, **kwargs):
        if kwargs.get('name'):
            self.username = kwargs['name']
        if kwargs.get('avatar_url'):
            self.avatar_url = kwargs['avatar_url']
        if kwargs.get('department'):
            self.department = kwargs['department']


class UserDetailInfo(Entity):
    username: str
    avatar_url: Optional[str]
    department: Optional[str]
    is_display: bool
    my_reaction: int = 0
    received_reaction_count: int

from typing import List, Optional

from fastapi import HTTPException, APIRouter

from app.applications.services.reaction_services import ReactionServiceImpl
from app.applications.services.user_services import UserServiceImpl
from app.domains.reactions.entities import UserReceivedEmojiInfo
from app.domains.users.schemas import UserCreateSchema
from app.domains.users.entities import UserDetailInfo


user_router = APIRouter()


@user_router.post("/", name="유저 생성 api", description="""
""", response_model=UserDetailInfo)
async def create_user(user_create_schema: UserCreateSchema):
    user = await UserServiceImpl.get_by_slack_id(slack_id=user_create_schema.slack_id)
    if user:
        raise HTTPException(status_code=400, detail="already registered")
    return await UserServiceImpl.create_user(user_create_schema.__dict__)


@user_router.get("/", name="전체 유저 리스트 반환 api", description="""
유저리스트를 반환합니다. 받은 reaction 이 높은 순으로 정렬합니다.
""", response_model=List[UserDetailInfo])
async def get_user(year: Optional[int] = None, month: Optional[int] = None, department: Optional[str] = None):
    users = await UserServiceImpl.get_detail_user(year=year, month=month, department=department)
    return users


@user_router.get("/{user_id}/reactions/", name="유저 리액션 반환 api", description="""
특정 유저가 받은 reaction 과 전달한 유저정보를 반환합니다.
""", response_model=List[UserReceivedEmojiInfo])
async def get_reactions(user_id: int = 0, year: Optional[int] = None, month: Optional[int] = None):
    return await ReactionServiceImpl.get_received_emoji_infos(user_id, year, month)


@user_router.get("/{slack_id}/my_reaction/", name="특정 유저가 받은 리액션 반환 api", description="""
특정 유저가 받은 reaction 정보를 전달합니다.
""")
async def get_my_reaction(slack_id: str = '', year: Optional[int] = None, month: Optional[int] = None):
    return await ReactionServiceImpl.count_reaction_data(slack_id, year, month)

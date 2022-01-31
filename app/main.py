from typing import List, Optional

from fastapi import FastAPI, HTTPException, Depends
from starlette.middleware.cors import CORSMiddleware

from app.dependency.requests import get_slack_event
from app.domain.schemas.reaction_schema import UserReceivedEmojiInfo
from app.domain.schemas.user_schema import User, UserDetailInfo

from app.services.reaction_service import ReactionService
from app.services.slack_service import SlackService
from app.services.user_service import UserService

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post(path="/slack", name='슬랙 웹훅 api')
async def slack(slack_event=Depends(get_slack_event)):
    response = await SlackService.slack_web_hook_handler(slack_event)
    return response


@app.post("/users/", name="유저 생성 api", description="""
""", response_model=UserDetailInfo)
async def create_user(user: User):
    user = await UserService.get_user(slack_id=user.slack_id)
    if user:
        raise HTTPException(status_code=400, detail="already registered")
    return await UserService.create_user(user=user)


@app.get("/users/", name="전체 유저 리스트 반환 api", description="""
유저리스트를 반환합니다. 받은 reaction 이 높은 순으로 정렬합니다.
""", response_model=List[UserDetailInfo])
async def get_user(year: Optional[int] = None, month: Optional[int] = None, department: Optional[str] = None):
    users = await UserService.get_detail_user(year=year, month=month, department=department)
    return users


@app.get("/users/{user_id}/reactions/", name="유저 리액션 반환 api", description="""
특정 유저가 받은 reaction 과 전달한 유저정보를 반환합니다.
""", response_model=List[UserReceivedEmojiInfo])
async def get_reactions(
    user_id: int = 0,
    year: Optional[int] = None,
    month: Optional[int] = None
):
    return await ReactionService.get_user_reactions(user_id, year, month)


@app.get("/users/{slack_id}/my_reaction/", description="""
특정 유저가 받은 reaction 정보를 전달합니다.
""")
async def get_my_reaction(
    slack_id: str = '',
    year: Optional[int] = None,
    month: Optional[int] = None
):
    return await ReactionService.get_my_reaction(slack_id, year, month)


@app.get("/")
async def read_root():
    return {"Hello": "World"}

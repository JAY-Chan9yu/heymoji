from typing import List, Optional

from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from app import schemas

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
async def slack(request: Request):
    request_event = await request.json()
    response = SlackService.check_challenge(request_event)
    return response


@app.post("/users/", name="유저 생성 api", description="""
""", response_model=schemas.User)
async def create_user(user: schemas.UserCreate):
    db_user = UserService.get_user(slack_id=user.slack_id)
    if db_user:
        raise HTTPException(status_code=400, detail="already registered")
    return UserService.create_user(user=user)


@app.get("/users/", name="전체 유저 리스트 반환 api", description="""
유저리스트를 반환합니다. 받은 reaction 이 높은 순으로 정렬합니다.
""", response_model=List[schemas.ReceivedReactionUser])
async def get_user(year: Optional[int] = None, month: Optional[int] = None):
    users = UserService.get_user_list(year=year, month=month)
    if not users:
        raise HTTPException(status_code=404, detail="Does Not Exists (User)")
    return users


@app.get("/users/{user_id}/reactions/", name="유저 리액션 반환 api", description="""
특정 유저가 받은 reaction 과 전달한 유저정보를 반환합니다.
""", response_model=List[schemas.UserReceivedReactions])
async def get_reactions(
    user_id: int = 0,
    year: Optional[int] = None,
    month: Optional[int] = None
):
    reactions = ReactionService.get_user_reactions(user_id, year, month)
    if not reactions:
        raise HTTPException(status_code=404, detail="Does Not Exists (User)")
    return reactions


@app.get("/users/{slack_id}/my_reaction/", description="""
특정 유저가 받은 reaction 정보를 전달합니다.
""")
async def get_my_reaction(
    slack_id: str = '',
    year: Optional[int] = None,
    month: Optional[int] = None
):
    reaction_info = ReactionService.get_my_reaction(slack_id, year, month)
    if not reaction_info:
        raise HTTPException(status_code=404, detail="Does Not Exists (User)")
    return reaction_info


@app.get("/")
async def read_root():
    return {"Hello": "World"}

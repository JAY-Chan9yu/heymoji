import sys
import os

# 모듈 경로를 못찾는 경우가 있어서 sys.path 에 경로 추가 (IDE를 사용하면 잘 찾음)
from schemas import ReceivedReactionUser

script_dir = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(script_dir) not in sys.path:
    sys.path.insert(0, os.path.dirname(script_dir))

from typing import Optional, List

from fastapi import FastAPI, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from services import SlackService
from conf.database import get_db, engine, Base
from app import crud, schemas


# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post(path="/slack")
async def slack(request: Request, db: Session = Depends(get_db)):
    """
    slack webhook api
    """
    request_event = await request.json()
    response = SlackService.check_challenge(request_event, db)

    return response


@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    user create api
    """
    db_user = crud.get_user(db, item_user=user.slack_id)

    if db_user:
        raise HTTPException(status_code=400, detail="already registered")

    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[ReceivedReactionUser],
         description="유저리스트를 반환합니다. 받은 reaction 이 높은 순으로 정렬합니다.")
async def get_user(
    db: Session = Depends(get_db),
    year: Optional[int] = None,
    month: Optional[int] = None
):
    """
    user get api
    """
    users = crud.get_users(db, year, month)

    if not users:
        raise HTTPException(status_code=404, detail="Does Not Exists (User)")

    return users


@app.get("/users/{user_id}/reactions/", response_model=List[schemas.UserReceivedReactions],
         description="특정 유저가 받은 reaction 과 전달한 유저정보를 반환합니다.")
async def get_reactions(
    db: Session = Depends(get_db),
    user_id: int = 0,
    year: Optional[int] = None,
    month: Optional[int] = None
):
    reactions = crud.get_reactions(db, user_id, year, month)

    if not reactions:
        raise HTTPException(status_code=404, detail="Does Not Exists (User)")

    return reactions


@app.get("/users/{slack_id}/my_reaction/", description="특정 유저가 받은 reaction 정보를 전달합니다.")
async def get_my_reaction(
    db: Session = Depends(get_db),
    slack_id: str = '',
    year: Optional[int] = None,
    month: Optional[int] = None
):
    reaction_info = crud.get_my_reaction(db, slack_id, year, month)

    if not reaction_info:
        raise HTTPException(status_code=404, detail="Does Not Exists (User)")

    return reaction_info


@app.get("/")
async def read_root():
    return {"Hello": "World"}

from fastapi import FastAPI, Request, Depends, HTTPException
from sqlalchemy.orm import Session

from api.services import SlackService
from conf.database import get_db, engine, Base
from models.users import schemas, crud

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.post(path="/slack")
async def slack(request: Request, db: Session = Depends(get_db)):
    request_event = await request.json()
    slack_service = SlackService()
    slack_service.check_challenge(request_event, db)

    return {}


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, item_user=user.slack_id)

    if db_user:
        raise HTTPException(status_code=400, detail="already registered")

    return crud.create_user(db=db, user=user)


@app.get("/")
def read_root():
    return {"Hello": "World"}

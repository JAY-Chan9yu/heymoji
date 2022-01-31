from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routers.slack import slack_router
from app.routers.users import user_router


def start_application():
    _app = FastAPI(dependencies=[])

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.include_router(user_router, prefix="/users", tags=["users"])
    _app.include_router(slack_router, prefix="/slack", tags=["slack"])

    return _app


app = start_application()


@app.on_event("startup")
async def startup_event():
    print("startup app")


@app.on_event("shutdown")
def shutdown_event():
    print("shutdown app")

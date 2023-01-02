from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.Infrastructure.database import on_startup, on_shutdown
from app.api.routers.slack import slack_router
from app.api.routers.users import user_router
from conf import settings


def start_application():
    _app = FastAPI(dependencies=[])

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.config.ALLOW_ORIGINS,
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
    on_startup()
    print("startup Heymoji")


@app.on_event("shutdown")
def shutdown_event():
    on_shutdown()
    print("shutdown Heymoji")

from .user import user_rt
from fastapi import FastAPI


def create_app():
    app = FastAPI()
    app.include_router(user_rt)
    return app
from .article.articlert import article_rt
from .user.userrt import user_rt
from fastapi import FastAPI


def create_app():
    app = FastAPI()
    app.include_router(article_rt)
    app.include_router(user_rt)
    return app
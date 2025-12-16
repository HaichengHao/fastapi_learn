from fastapi import APIRouter

article_rt = APIRouter(
    prefix="/article",
    tags=["article"],
)

@article_rt.get('/')
async def article():
    return {
        'msg':'文章路由被调用!!'
    }

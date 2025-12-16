from fastapi import APIRouter

user_rt = APIRouter(
    prefix="/user",
    tags=["user"],
)

@user_rt.get('/')
async def user():
    return {
        'msg':'用户路由被调用!!'
    }

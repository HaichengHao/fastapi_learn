from fastapi import APIRouter

user_rt = APIRouter(
    prefix="/user",
    tags=["user"],
)

@user_rt.get("/")
async def get_user():
    return {"message": "我是用户路由，我被调用了"}
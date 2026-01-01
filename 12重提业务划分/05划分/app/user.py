# @Time    : 2026/1/1 22:23
# @Author  : hero
# @File    : user.py

from fastapi import APIRouter
from models import UserTB
from schema import Userschema
user_router = APIRouter()



@user_router.post('/create')
async def create_user(user: Userschema):
    # await UserTB.create(
    #     username=user.username,
    #     email=user.email,
    #     age=user.age
    # )
    # tips:其实这样写是有些麻烦的，我们可以用一个简单的方式,和上面的效果是一样的,
    # important：⚠️但是这个有要求，就是schema字段的名称要和数据表字段的名称一致
    user_new = await UserTB.create(
        **user.model_dump()
    )
    return user_new


# 获取第一条用户的信息,
# tips:前端可能不关心字段，所以像这个“第一条”测试，只需要返回部分字段检验成功与否
@user_router.get('/info')
async def get_user_info():
    user = await UserTB.first()  # tips:从数据表中读取第一条数据，要知道表UserTB字段有5个
    user_schema = Userschema.model_validate(user.__dict__)  # tips:但是返回的时候只返回Userschema中的3个
    return user_schema

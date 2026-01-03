# @Time    : 2026/1/2 21:08
# @Author  : hero
# @File    : main.py
from typing import Annotated

#tips:所谓路由级的依赖注入就是将其注册到整个路由当中
# 譬如，对用户数据做任何操作时都要检查token
from fastapi import FastAPI, Depends, APIRouter, Header, HTTPException

app = FastAPI()
async def check_auth(token:Annotated[str,Header(...)]):
    if token != 'linuxforlinkeverythings':
        raise HTTPException(status_code=401, detail='Unauthorized')
    else:
        return {
            'user':'admin'
        }


user_router = APIRouter(dependencies=[Depends(check_auth)]) #tips：为整个user路由注入依赖



#tips:进行了路由级别的注册之后，其下的路由都受到了保护

@user_router.get('/admin/dashboard')
async def admin_dashboard():
    return {
        'message':'welcome to admin dashboard'
    }

@user_router.get('/users')
async def admin_user():
    return {
        'users':'userinfo'
    }


app.include_router(user_router,prefix='/user',tags=['用户路由'])



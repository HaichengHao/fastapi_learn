# @Time    : 2026/1/2 20:10
# @Author  : hero
# @File    : main.py

from fastapi import FastAPI, Depends, Header, HTTPException,status,Query
from typing import Annotated
app = FastAPI()

#tips:定义一个函数检查token
def  check_user_permission(token:str=Header(...)): #tips:回顾一下，点点点是未写参数但是必填的意思
    if  token!='secret-token': #tips:这里没单独生成token,先用个假的'secret-token'替代
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid token'
        )
    return {
        'user':'admin'
    }

@app.get("/admin/",dependencies=[Depends(check_user_permission)])
async def  admin_dashbord():
    return {
        'message':'welcome to admin dashboard'
    }

#tips:定义一个获取分页的参数
def get_pagination_params(
        page:int=Query(1,g1=1),
        page_size:int=Query(10,g1=1,le=100)
):
    return {
        'page':page,
        'page_size':page_size,
    }

@app.get('/items/')
async def  get_items(pagination:int=Depends(get_pagination_params)):
    return {
        'items':[f'item{i}' for i in  range(1,4)],
        'current_page':pagination['page'],
        'page_size':pagination['page_size'],
    }

# @Time    : 2026/1/3 17:12
# @Author  : hero
# @File    : main.py

from fastapi import FastAPI, Header, HTTPException,status,Depends
from typing import Annotated

def check_auth(token:Annotated[str,Header(...)]): #tips:这里用更优美的fastapi的写法
    if token!='hahaha':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Invalid token')
    else:
        return token
def get_current_user(token:Annotated[str,Depends(check_auth)]): #tips:先进行依赖注入，看看token是否正确
    return {
        'user':'admin',
        'token':token
    }


app  =  FastAPI()

@app.get('/user')
async def get_user(user:Annotated[dict,Depends(get_current_user)]):
    return user

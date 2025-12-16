'''
请求体解决的问题
1.如果只是写在查询参数或者路径参数中，那么返回的是明文，不利于保密
2.路径参数和查询参数携带的数据是有限的
'''
from typing import Annotated

#tips:fastapi使用请求体从客户端向api发送数据(譬如post请求)

# 发送数据使用post,put,delete,patch(局部更新) 等操作
from fastapi import FastAPI
from pydantic import BaseModel

class User(BaseModel):
    uid:int
    uname:str
    uaddress:str



app = FastAPI()

@app.post('/users')
async def create_user(user:User): #tips:定义一个类似于创建用户的请求
    return user


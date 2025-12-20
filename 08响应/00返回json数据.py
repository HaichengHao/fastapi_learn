# @Time    : 2025/12/18 12:45
# @Author  : hero
# @File    : 00返回json数据.py


#tips:fastapi是支持字典的，可以直接返回json格式
#tips:我们也可以用response_model来为其定制返回模型



from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Annotated
app = FastAPI()

@app.get('/')
async def root():
    return {
        'name': 'root',
        'age':18
    }



#tips:或者来一个现实点的例子
class User(BaseModel):
    name: str
    age: Annotated[int,Field(ge=18,le=80)]
    pwd: Annotated[str,Field(max_length=10,min_length=6,description='输入6-10位密码')]
    hobby:str|None=None

#tips:定义返回模型
class Response(BaseModel):
    name: str
    age: Annotated[int,Field(ge=18,le=80)]



@app.post('/useradd',description='添加用户信息',response_model=Response)#tips:在这里指定返回值类型
async def useradd(user: User): #tips:输入的时候还是要按照我们指定的User来输入
    return user
"""
{
  "name": "nikofox",
  "age": 18
} 可以看出，响应的就是我们指定的返回模型的定义格式
"""

@app.get('/users',response_model=User,response_model_exclude_unset=True)#tips:⬅️response_model_exclude_unset意思是排除掉未设置的
async def adduser():
    return User(name='nikofox',age=18,pwd='nionionio')
"""
{
  "name": "nikofox",
  "age": 18,
  "pwd": "nionionio"
}  因为我们设置了response_model_exclude_unset这样一来我们没写的就不会给我们返回了
"""

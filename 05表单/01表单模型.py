# @Time    : 2025/12/17 10:20
# @Author  : hero
# @File    : 01表单模型.py
'''
看上面表单数据我们可以感受到它写起来还是很不优雅的
所以我们直接使用表单模型
'''

from fastapi import FastAPI,Form
from pydantic import BaseModel,Field,field_validator
from typing import Annotated
import re
app = FastAPI()

class User(BaseModel):
    name:Annotated[str,Field(min_length=3,max_length=20)]
    phone_num:str
    @field_validator('phone_num')
    def validate_phone_num(cls, v):
        pattern=r'^1[3-9]\d{9}$'
        if re.match(pattern,v):
            return v
        else:
            return '格式有问题'
    age:Annotated[int,Field(le=100,ge=18)]


@app.post('/users')
async def create_user(user:Annotated[User,Form()]):
    return user

# @Time    : 2025/12/17 08:54
# @Author  : hero
# @File    : 02请求体Field验证.py
'''
这里也是没有按照官方文档的顺序
这个Field是在01路径参数Path之后，即在04Query之后
'''
import re
import uvicorn
from typing import Annotated
from fastapi import FastAPI
from pydantic import BaseModel, Field, BeforeValidator, field_validator, EmailStr, HttpUrl

app = FastAPI()

'''
还有另一种验证基础邮箱地址的方式
pip install email-validator
from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    email: EmailStr  # 自动验证标准邮箱格式
'''

#tips:方式1
class User(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=9, description='长度为3-9')]
    # email: Annotated[str, BeforeValidator(validator_email)]
    email: str

    # tips:还有一种验证方式,这是文档推荐的官方方式,从pydantic引入field_validator来验证需要的字段
    @field_validator('email')
    def validate_email(cls, value):
        ptn = r'^[A-Za-z0-9_\-\.]+@(163\.com|qq\.com|42du\.cn)$'
        if re.match(ptn, value, re.S):
            return value
        else:
            return '格式有问题,请重新输入'

    address: Annotated[str, Field(description='输入地址', min_length=3, max_length=25, example='如xx市xx区')]
    phone_num: Annotated[str, Field(pattern=r'^1[3-9]\d{9}$', description='输入正确的格式')]
    age: Annotated[int, Field(ge=18, le=100)]


@app.post('/users', description='用户创建')
async def create_user(user: User):
    return user



#tips:方式2

def validator_email(value):
    pattern = r'^[A-Za-z0-9_\-\.]+@(163\.com|qq\.com|42du\.cn)$'
    if re.match(pattern, value, re.S):
        return value
    else:
        return '邮箱地址格式有问题'
class User2(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=9, description='长度为3-9')]
    email: Annotated[str, BeforeValidator(validator_email)]
    address: Annotated[str, Field(description='输入地址', min_length=3, max_length=25, example='如xx市xx区')]
    phone_num: Annotated[str, Field(pattern=r'^1[3-9]\d{9}$', description='输入正确的格式')]
    age: Annotated[int, Field(ge=18, le=100)]


@app.post('/users2', description='用户创建')
async def create_user(user: User2):
    return user


class Order_lst(BaseModel):
    oid:int
    olst:Annotated[list[str],Field(min_length=3,max_length=25)]

@app.post('/orderlst')
async def create_orderlst(orderlst: Order_lst):
    return orderlst


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image] | None = None #tips:含有子模型的列表类型


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8099)

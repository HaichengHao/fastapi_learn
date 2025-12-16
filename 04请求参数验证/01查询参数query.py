# @Time    : 2025/12/16 14:22
# @Author  : hero
# @File    : 01查询参数query.py
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


# important:注意，query用在查询参数上，别用在路径参数上
@app.get('/users/')
async def get_user(phone_num: Annotated[
    int | str, Query(alias='shoujihao', pattern='^1[3-9]\d{9}$', title='输入正确的手机号',
                     description='手机号默认11位，别输错了')]):
    return {'phonenum': phone_num}


@app.get('/guss/')
async def get_guss(num: Annotated[int, Query(ge=5, le=10, title='数字不在规定范围内就会出错哦！！',description='输入一下',deprecated=True)]): #它也可以像在get中写过期标识
    return {'num': num}


@app.get('/goods')
async def get_goods(gid: Annotated[int, Query(...)]):  # tips:这里写的意思就是必须传递的查询参数的意思，一般不要这样写
    return {'gid': gid}


@app.post('/guss/')
async def age_edit(age: Annotated[int, Query(ge=0, le=100, title='输入年龄')]):
    return {'age': age}


@app.post('/getfloatnum')
async def float_num_get(fnum: Annotated[float, Query(ge=5.0, le=10.0,deprecated=True)]):
    return {'fnum': fnum}


@app.post('/getfloatnum2')
async def flnum(float_num: Annotated[float, Query(ge=5.0, le=10.0, alias='fnum')]):  # tips:可以给输入框中的place_holder换个名字罢了
    return {'fnum': float_num} #tips:后态逻辑还是用非别名

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

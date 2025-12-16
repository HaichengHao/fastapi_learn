# @Time    : 2025/12/16 14:22
# @Author  : hero
# @File    : 01查询参数query.py
from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()

#important:注意，query用在查询参数上，别用在路径参数上
@app.get('/users/')
async def get_user(phone_num: Annotated[
    int|str, Query(alias='shoujihao',regex=r'^1[3-9]\d{9}$', title='输入正确的手机号', description='手机号默认11位，别输错了')]):
    return {'id': phone_num}

# @Time    : 2026/1/2 16:03
# @Author  : hero
# @File    : main.py
from typing import Annotated

from fastapi import FastAPI,Depends
app = FastAPI()

#简单依赖函数,定义一个函数实现将请求字段转为大写
def get_query_param(q:str='default'):
    return q.upper()




@app.get("/items/")
async def read_items(query:Annotated[str,Depends(get_query_param)]):
    return {'query': query}


def multiparams(name:str,age:str,clazz:str):
    return {
        'name':name,
        'age':age,
        'clazz':clazz
    }

@app.get('/demo')
async def get_params(params:Annotated[dict,Depends(multiparams)]):
    return {
        'params':params
    }
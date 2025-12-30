# @Time    : 2025/12/29 14:04
# @Author  : hero
# @File    : main.py

from  fastapi import FastAPI

app =FastAPI()


@app.middleware('http')
async def middleware2(request,call_next):
    print('中间件2开始')
    response = await call_next(request)
    print('中间件2处理结束')
    return response

@app.middleware("http")
async def middleware1(request,call_next):
    print('中间件1开始')
    response = await call_next(request)
    print('中间件1处理结束')
    return response



@app.get('/')
async def index():
    print('开始处理逻辑')
    return {'msg':'hello world'}
# @Time    : 2025/12/29 13:09
# @Author  : hero
# @File    : main.py

from fastapi import FastAPI,Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# tips:定义中间件,注意必须传入request参数
#  call_next表示的是向下传递请求

@app.middleware('http')
async def middlware1(request, call_next):
    print('业务来了，准备处理')
    print(request.method,request.url)
    # if request.url.path == '/':
    #     return Response('你无权访问')
    response = await call_next(request)
    response.headers['X-Token']='121212'
    print('业务处理好了')
    return response


@app.get('/')
async def root():
    print('处理中')
    return {
        'msg': 'hello'
    }

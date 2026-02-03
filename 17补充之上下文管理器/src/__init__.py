"""
@File    :__init__.py.py
@Editor  : 百年
@Date    :2026/2/9 19:40 
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
from cr_asyncengine import init_db

@asynccontextmanager
async def life_span(app: FastAPI):
    print('服务器正在启动')
    await init_db()
    yield
    print('服务器已经停止')

version='v1.0.0'
app = FastAPI(
    title='测试',
    description='用于书籍仓储服务',
    version=version,
    lifespan=life_span
)


# @Time    : 2026/1/6 13:34
# @Author  : hero
# @File    : main.py

import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from route import v1_router


@asynccontextmanager
async def life_span(app: FastAPI):
    print(f'server is starting...')
    yield app
    print(f'server is stopped...')


app = FastAPI(
    title='booksys',
    description='图书管理用后端接口',
    version='0.0.1',
    lifespan=life_span
)
app.include_router(v1_router, prefix="/v1")

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8099, reload=True)

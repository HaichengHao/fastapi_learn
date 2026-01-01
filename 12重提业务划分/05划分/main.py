# @Time    : 2026/1/1 22:19
# @Author  : hero
# @File    : main.py

import uvicorn
from fastapi import FastAPI
from database import register_db
from app import v1_router
from config  import Tortoise_orm
from  middleware  import add_cors_middleware,request_middleware
app = FastAPI()
add_cors_middleware(app)
request_middleware(app)
app.include_router(v1_router,prefix='/apis/v1',tags=['v1'])
register_db(app,config=Tortoise_orm,generate_schemas=False,add_exception_handlers=True)

if __name__ == '__main__':
    uvicorn.run('main:app',host='127.0.0.1',port=8099,reload=True)
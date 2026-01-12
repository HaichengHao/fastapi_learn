# @Time    : 2025/12/29 09:41
# @Author  : hero
# @File    : main.py
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from settings import Tortoise_orm
import uvicorn
from apps.stuapi.stu import stu_router

app = FastAPI()

register_tortoise(
    app=app,
    config=Tortoise_orm,
    # generate_schemas=True,  # tips:这是一定要写的，但是本例子中只是操作已经有的表，所以不用再次生成了
    # add_exception_handlers=True
)
app.include_router(stu_router, prefix='/students')


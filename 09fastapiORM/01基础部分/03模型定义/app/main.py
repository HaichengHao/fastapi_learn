# @Time    : 2025/12/22 10:18
# @Author  : hero
# @File    : main.py
from fastapi import FastAPI
from .aerichconfig import Tortoise_orm
from tortoise.contrib.fastapi import register_tortoise
app = FastAPI()

register_tortoise(
    app,
    config=Tortoise_orm,
    generate_schemas=True,
    add_exception_handlers=True
)

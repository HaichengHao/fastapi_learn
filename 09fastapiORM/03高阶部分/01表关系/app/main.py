# @Time    : 2025/12/25 09:50
# @Author  : hero
# @File    : main.py

from fastapi import FastAPI
from config import Tortoise_orm
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()
register_tortoise(
    app,
    config=Tortoise_orm,
    generate_schemas=True,
    add_exception_handlers=True
)

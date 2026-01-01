# @Time    : 2026/1/1 22:21
# @Author  : hero
# @File    : database.py

from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI
def register_db(app:FastAPI,config:dict,generate_schemas:bool=True,add_exception_handlers:bool=True):
    register_tortoise(
        app=app,
        config=config,
        generate_schemas=generate_schemas,
        add_exception_handlers=add_exception_handlers
    )
# @Time    : 2026/1/1 22:22
# @Author  : hero
# @File    : __init__.py.py

from fastapi import FastAPI, APIRouter
from .user import user_router
from .item import item_router

v1_router = APIRouter()
v1_router.include_router(item_router,prefix='/item')
v1_router.include_router(user_router,prefix='/user')

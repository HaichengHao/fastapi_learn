# @Time    : 2026/1/6 13:40
# @Author  : hero
# @File    : __init__.py.py

from fastapi import APIRouter
from route.book.api import book_api

v1_router = APIRouter()

v1_router.include_router(book_api, prefix="/book", tags=["book"])

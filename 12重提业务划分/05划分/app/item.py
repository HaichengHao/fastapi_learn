# @Time    : 2026/1/1 22:23
# @Author  : hero
# @File    : item.py

from fastapi import APIRouter
item_router = APIRouter()

#定义item的路由
@item_router.get('/info')
async def get_item_info():
    return '商品信息'



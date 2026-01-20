# @Time    : 2026/1/6 13:42
# @Author  : hero
# @File    : api.py

from  fastapi import APIRouter
from  .schema import BookSC,BookUpateSC
book_api = APIRouter()

@book_api.get('/',response_model=list[BookSC])
async def get_allbooks():
    pass

@book_api.get('/{id}',response_model=BookSC)
async def get_book(id: int):
    pass

@book_api.post('/')
async def create_book(book:BookSC):
    pass

@book_api.put('/{id}')
async def update_book(id:int,book:BookUpateSC):
    pass

@book_api.delete('/{id}')
async def delete_book(id:int):
    pass
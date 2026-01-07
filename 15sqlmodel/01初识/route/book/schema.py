# @Time    : 2026/1/6 13:31
# @Author  : hero
# @File    : schema.py

from pydantic import BaseModel

class BookSC(BaseModel):
    id:int
    title: str
    author:str
    publisher:str
    page_count:int
    language:str

class BookUpateSC(BaseModel):
    title:str
    author:str
    publisher:str
    page_count:int
    language:str
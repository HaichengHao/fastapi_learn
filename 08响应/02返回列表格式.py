# @Time    : 2025/12/18 14:39
# @Author  : hero
# @File    : 02返回列表格式.py
from fastapi import FastAPI
from typing import Annotated
from typing import List

from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name:str
    id:int

@app.post("/items")
async def get_item1(items: List[Item]): #tips:指定返回的类型是列表，列表中的元素是Item对象
    return items



@app.post("/items",response_model=List[Item])
async def get_item2(items: List[Item]):
    return items
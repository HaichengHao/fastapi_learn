# @Time    : 2025/12/18 15:08
# @Author  : hero
# @File    : 03数据过滤与分页.py

from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()


# tips:先构建一个伪造数据方便我们进行代码编写

class Item(BaseModel):
    id: int
    name: str
    price: float
    category: str


data = [Item(id=i, name=f'Apple{i}', price=100.0 * i, category='ipad' if i % 2 == 0 else 'iphone') for i in
        range(1, 21)]


@app.get("/items", response_model=list[Item])
async def get_items():
    return data


# tips:然后来个数据过滤
@app.get('/items_specify', response_model=list[Item])
async def get_items_specify(category_: Annotated[str, Query(description='输入种类')]):
    if category_:
        return [item for item in data if item.category == category_]
    else:
        return data


# tips:再来一个处理分页的
# 注意，处理分页的思路是接收一个页数(page)和per_page_count,这是flask中那种
@app.get('/items_pagi', response_model=list[Item])
async def get_items_pagi(
        category_: Annotated[str, Query(description='输入种类')],
        page: Annotated[int, Query(ge=1, description='输入页码')] = 1,
        page_size: Annotated[int, Query(ge=1, le=5, description='每页要展示的数量')] = 5,

):
    if category_:
        filterd_item = [item for item in data if item.category == category_]

    count_items = len(filterd_item)
    total_pages = (count_items + page_size - 1) // page_size  # tips:计算总共需要多少页
    if total_pages:  #tips:下面定义起始页数
        start = (page - 1) * page_size
        end = start + page_size

        return filterd_item[start:end]
    else:
        return filterd_item[:page_size]

# @Time    : 2025/12/18 17:23
# @Author  : hero
# @File    : 04分页的封装.py


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


class Pagination(BaseModel):
    total: int
    page: int
    per_page_size: int
    total_pages: int


class ListResponse(BaseModel):
    status: str = 'success'
    items: list[Item]
    pagination: Pagination


data = [Item(id=i, name=f'Apple{i}', price=100.0 * i, category='ipad' if i % 2 == 0 else 'iphone') for i in
        range(1, 21)]

@app.get('/items')
async def get_items_pagi(
        category_: Annotated[str, Query(description='输入种类')],
        page: Annotated[int, Query(ge=1, description='输入页码')] = 1,
        page_size: Annotated[int, Query(ge=1, le=5, description='每页要展示的数量')] = 5,

):
    if category_:
        filterd_item = [item for item in data if item.category == category_]

    count_items = len(filterd_item)
    total_pages = (count_items + page_size - 1) // page_size  # tips:计算总共需要多少页
    if total_pages:  # tips:下面定义起始页数
        start = (page - 1) * page_size
        end = start + page_size

        return ListResponse(
            status='success',
            items=filterd_item[start:end],
            pagination=Pagination(
                total=count_items,
                total_pages=total_pages, page=page, per_page_size=page_size)
        )
    else:
        return filterd_item[:page_size]

''' 其实本节就是嵌套了模型
{
  "status": "success",
  "items": [
    {
      "id": 2,
      "name": "Apple2",
      "price": 200,
      "category": "ipad"
    },
    {
      "id": 4,
      "name": "Apple4",
      "price": 400,
      "category": "ipad"
    },
    {
      "id": 6,
      "name": "Apple6",
      "price": 600,
      "category": "ipad"
    },
    {
      "id": 8,
      "name": "Apple8",
      "price": 800,
      "category": "ipad"
    },
    {
      "id": 10,
      "name": "Apple10",
      "price": 1000,
      "category": "ipad"
    }
  ],
  "pagination": {
    "total": 10,
    "page": 1,
    "per_page_size": 5,
    "total_pages": 2
  }
}'''
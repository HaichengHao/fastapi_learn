from typing import Annotated

from fastapi import FastAPI

app = FastAPI()
#important：注意，查询参数如果没写默认值那就是必填参数

@app.get('/items/{item_id}')  # 路径参数就是直接拼接到路径当中的,而查询参数则是类似随着get请求传来的
# tips:如 https://cn.bing.com/search?q=周星驰 这个?后面跟着的就是查询参数q
# 如果有多个查询参数，那么它们的路由将通过&符号拼接在一起
# https://cn.bing.com/search?q=周星驰&PC=U316&FORM=CHROMN
async def read_items(item_id: int, item_name: str | None = None): #指定查询参数是str类型，没写就为None,默认值为None
    return {'item_id': item_id, 'item_name': item_name}

"""
{
  "item_id": 12,
  "item_name": "周杰伦" 如果自己写了就有
}

{
  "item_id": 12,
  "item_name": null 没写的话就为默认的null,空字符串
}
"""
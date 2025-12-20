# @Time    : 2025/12/18 13:27
# @Author  : hero
# @File    : 01扩展之泛型.py


from fastapi import FastAPI

from typing import Annotated, Union, TypeVar,Generic

from pydantic import BaseModel
# from typing_extensions import Generic

app = FastAPI()


class Item(BaseModel):
    id: int
    name: str
    tags: list[str] = []


# tips:定义泛型模型
T = TypeVar('T') #创建一个占位符类型，叫 T


class SuccessResponse(BaseModel, Generic[T]): #Generic[T]告诉 Pydantic/Python：“我这个类是个泛型，具体类型在使用时确定”。
    status:str='success'
    data: T #data 字段的类型不是固定的，而是你传什么就是什么。
class ErrorResponse(BaseModel):
    status:str='error'
    message: str
    code: int


#important：下面这个SuccessResponse[Item]表示这是一个SuccessResponse类型的对象，它的泛型函数T被指定为Item
#  简单理解，SuccessResponse[]是两片面包,【】中间就是它要夹的东西
@app.get("/item/{item_id}", response_model=Union[SuccessResponse[Item],ErrorResponse])#tips:诉 FastAPI，这个接口可能返回 A 或 B。
async def get_item(item_id: int):
    if item_id == 1:
        item = Item(id=1,name='iphone',tags=['red','blue','black'])
        return SuccessResponse[Item](data=item)  #important这个()括号里头就是面包
    else:
        return ErrorResponse(message='未找到',code=404)
"""
{
  "status": "success",
  "data": {
    "id": 1,
    "name": "iphone",
    "tags": [
      "red",
      "blue",
      "black"
    ]
  }
}"""

"""如果输入的id不是1
{
  "status": "error",
  "message": "未找到",
  "code": 404
}"""
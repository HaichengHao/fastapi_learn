import uvicorn
from fastapi import FastAPI

from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    id: int
    name: str
    address: str


@app.get('/user',deprecated=True) #tips:看看源码中其实有很多很有意思的参数,把鼠标移动到get上就能看见
async def read_user(user: User):
    return user


@app.get('/items/{item_id}')
async def read_item(item_id: int):
    # tips:这里就是类型注解，即标记参数的类型，如果标记之后就会是我们标记的类型，如果传入的类型不是int的话就会报错
    return {'item_id': item_id}


@app.get('/items2/{item}')
async def read_items2(item: int | str):  # tips:我们也可以使用union这样的注解，这样就支持两种类型
    return {'item': item}

@app.get('/items3/{item_id}')
async def read_items3(item_id: int|str ,item_name:str|None=None): #tips:注意，路径参数是不能设置默认值的，但是查询参数可以
    '''注意item_id是必须传递的'''
    return {'item_id': item_id,'item_name': item_name}
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8099)

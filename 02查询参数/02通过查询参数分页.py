from typing import Annotated

from fastapi import FastAPI

app = FastAPI()


@app.get('/q')
async def q(name: str, page: int | None = 1, limit: int | None = 5):
    return {'name': name, 'page': page, 'limit': limit}

'''
{
  "name": "nikoko", #这个是必须要填的，因为我们指定为str了，而且无默认值
  "page": 1,  #不填就用默认的
  "limit": 5 #同上 
}
'''
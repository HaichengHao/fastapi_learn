import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'Hello World'}
@app.get('/hello/{user_id}')
async def hello(user_id: int):
    return {
        'msg': 'Hello {}'.format(user_id)
    }
@app.get('/hello/{id}')
async def hello1(id: int):  #tips:这样只匹配上面的那一个，这个路由是不会被匹配到的
    return {
        'msg': 'Helloha {}'.format(id)
    }

@app.get('/hello/{id}/{name}')
async def hello2(id:int, name: str):
    #注意,如果我们不指定类型的话，这里就能看到返回的是字符串形式的id{"id":"12","name":"nikoko"}，
    # 但如果我们指定为int,则会返回我们指定的类型{"id":12,"name":"nikoko"}
    return {'id':id,'name':name} #
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8898)
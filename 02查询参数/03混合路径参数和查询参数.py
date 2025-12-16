from fastapi import FastAPI
import uvicorn
app = FastAPI()

@app.get('/user/{userid}')
async def index(userid: str,love_num:int|None=10,page:int|None=1):
    return {'userid': userid, 'love_num': love_num, 'page': page}
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8898)

'''
http://127.0.0.1:8898/user/888?love_num=10&page=1
可以看到我们的路径参数确实归于路径参数中了，查询参数以?的方式拼接'''
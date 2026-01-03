# @Time    : 2026/1/3 16:48
# @Author  : hero
# @File    : main.py

from fastapi  import FastAPI,Depends,Request

def logrequest(requset:Request):
    print(f'request received: {requset.method} {requset.url}')
    return {
        'logged':True
    }
app =  FastAPI(dependencies=[Depends(logrequest)])

@app.get('/items')
async def read_item():
    return {
        'items':'item successfuly geted'
    }

@app.get('/user')
async def read_user():
    return {
        'user':'user successfuly geted'
    }
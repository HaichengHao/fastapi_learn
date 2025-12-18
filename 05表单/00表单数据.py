# @Time    : 2025/12/17 10:15
# @Author  : hero
# @File    : 00表单数据.py
'''
首先需要$ pip install python-multipart
form的出现就是为了和json数据区分开
还有就是如果不写表单格式那么我们之前的post写法其实是还会拼接到查询参数中的
'''

from fastapi import FastAPI, Form
from typing import Annotated

app = FastAPI()

@app.post('/goods')
async def up_goods(gid:str,gname:str):
    return {
        'gid':gid,
        'gname':gname
    }
'''
curl -X 'POST' \
  'http://127.0.0.1:8099/goods?gid=121&gname=nio' \ <---可以看到还是会拼接到查询参数中
  -H 'accept: application/json' \
  -d ''
  '''

@app.post('/users/')
async def get_user(phone_num: Annotated[str, Form()], pwd: Annotated[str, Form()],
                   age: Annotated[int, Form(le=100, ge=18)]):
    return {'phonenum': phone_num, 'age': age}
'''
curl -X 'POST' \
  'http://127.0.0.1:8099/users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \ <--而且格式也是表单格式
  -d 'phone_num=19982917291&pwd=1212312&age=19' <--它就不一样了，不会代到查询参数中去
  
  '''
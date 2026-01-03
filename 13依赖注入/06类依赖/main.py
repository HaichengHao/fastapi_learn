# @Time    : 2026/1/3 18:07
# @Author  : hero
# @File    : main.py

from fastapi  import FastAPI,Depends
from typing import Annotated


class UserService:
    def __init__(self,db_connection:str):
        self.db_connection = db_connection

    def get_user(self,userid:int):
        return {
            'userid':userid,
            'db_connection':self.db_connection
        }


def get_user_service():
    return UserService(db_connection='mysql://niko:HHCzio20@localhost:3306/stusys')

app = FastAPI()

@app.get('/users/{userid}')
async def read_users(userid:int,user_service:Annotated[UserService,Depends(get_user_service)]):
    return user_service.get_user(userid)



# @Time    : 2026/1/1 22:36
# @Author  : hero
# @File    : schema.py

from pydantic import BaseModel
# tips:schema定义,输入输出校验
class Userschema(BaseModel):
    username: str
    email: str
    age: int
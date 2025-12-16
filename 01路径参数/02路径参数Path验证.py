# @Time    : 2025/12/16 21:41
# @Author  : hero
# @File    : 02路径参数Path验证.py

'''
这里我自己作了一个区分，因为fastapi文档的顺序容易让人迷惑
这里其实是04请求参数验证之后的一节，但是放到路径参数这里并无不妥
Path的参数其实很多和Query,Body都是相似的
'''
from typing import Annotated

from fastapi import FastAPI,Path
from pydantic import BaseModel,Field,AfterValidator,BeforeValidator #tips:AfterValidator和BeforeValidator是非常好用的两个验证器

app = FastAPI()

@app.get('/user/{age}',description='输入年龄判断可否访问')
async def get_user(age:Annotated[int,Path(ge=18,alias='年龄',description='输入年龄')]):
    if age>18 & age<100:
        return {
            'msg':'欢迎访问'
        }
    elif age<1:
        return {
            'msg':'对不起，认证错误'
        }
    else:
        return {
            'msg':'拜拜'
        }


#important:自己定义一个验证函数，然后用验证器调用该函数
def start_with_z(value):
    if value.startswith('z'):
        return value
    else:
        return '不是哦'

#tips:定义一个路由来实现判断输入的字符串是否以z开头
@app.get('/startwithz',description='判断输入的字符串是不是以Z开头')
async def start_with_z(ustr:Annotated[str,BeforeValidator(start_with_z)]): #tips:前验证器可以让在输入验证前判断
    return {
        'msg':ustr
    }



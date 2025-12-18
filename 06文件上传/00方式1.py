# @Time    : 2025/12/17 12:25
# @Author  : hero
# @File    : 00方式1.py
"""
这是方式1,用的是byte,和File配合的方式
"""
import os
from fastapi import FastAPI,File
from typing import Annotated
from pydantic import BaseModel,Field

app = FastAPI()

@app.post('/create_file/')
async def create_file(file:Annotated[bytes,File()]): #tips:注意，文件是二级制格式的，所以要指定为bytes格式

    return {
        # 'name':file.filename, important：注意，这样并不是我们之前flask那种filestorge格式，所以不推荐用这个，看下一个
        'size':len(file)
    }





'''
它不好的地方就是它会把数据加载到内存中，对大文件不友好，所以它只适合小文件
'''
# @Time    : 2025/12/17 13:00
# @Author  : hero
# @File    : 02多个文件上传方式1.py
import aiofiles
from fastapi import APIRouter, File, FastAPI
from typing import List

app = FastAPI()


@app.post('/')
async def get_file(files: List[bytes] = File()):  # important:文件是字节流,所以类型应该是bytes,并且默认应该是File对象
    for idx,file in enumerate(files):
        print("filename",files)
        with open(f'./demo{idx}.png','wb') as f:
            f.write(file)
    return {
        "length":len(files)
    }

#tips:下面的代码是错的！！，bytes对象无法进行异步流式读取，还是得用uploadfile
# @app.post('/uploadfile')
# async def upload_file(files:List[bytes] = File(...)):
#     for idx,file in enumerate(files):
#         async with aiofiles.open(f'./demo{idx}.png','wb') as f:
#             while chunk:=await file.read(1024*1024):
#                 await f.write(chunk)
#             return {
#                 'msg':'success'
#             }
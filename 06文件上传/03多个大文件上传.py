# @Time    : 2025/12/17 13:07
# @Author  : hero
# @File    : 03多个大文件上传.py
from fastapi import FastAPI, UploadFile, File
from typing import Annotated
import os
import aiofiles
import uuid as uuidlib

app = FastAPI()


@app.post('/upload_file')
async def upload_file(files: list[UploadFile]=File(...)): #tips:后面的=File(...)是依赖注入
    file_dir = './demopic'
    os.makedirs(file_dir, exist_ok=True)  # tips:更安全的创建目录方式

    for file in files:
        safe_filename = f"{uuidlib.uuid4().hex}{os.path.splitext(file.filename)[1]}" #tips:os.path.splitext(file.filename)[1]这个是拿到后缀
        fpath = os.path.join(file_dir, safe_filename)  # tips:构造路径

        async with aiofiles.open(fpath, 'wb') as f:  # important:用异步方式打开
            # while True: #tips:写一个死循环
            #     chunk = await file.read(1024 * 1024)  # 每次读取1MB
            #     if not chunk: break  # 如果chunk为空，也就是读取完毕之后，就终止循环
            #     await f.write(chunk)
            while chunk := await file.read(1024 * 1024): await f.write(chunk)  # tips:或者精简为一行，利用海象符号,这一行和上面的四行等价
            '''
            := 让你“边赋值，边使用”，特别适合：
            循环条件中需要先获取值再判断
            避免重复调用同一个函数'''
    return {
        'msg': '文件上传成功',
        'info': [file.filename for file in files],
        'sum':len(files)
    }



#tips:限制上传格式
@app.post('/uploadpic_strict')
async def upload_pic_strict(files: list[UploadFile]=File(...)):
    file_dir = './demopic'
    os.makedirs(file_dir, exist_ok=True)
    #tips:定义限定后缀
    suffix_allowd=['png','jpg','jpeg']
    #tips:定义允许列表,记录允许的文件
    allowed=[]
    #tips:定义不被允许列表，记录不被允许的文件
    not_allowed=[]

    for file in files:
        file_suffix = file.filename.split('.')[-1]
        if file_suffix in suffix_allowd:
            allowed.append(file.filename) #tips:添加到允许列表中方便记录
            safe_filename = f"{uuidlib.uuid4().hex}{os.path.splitext(file.filename)[1]}" #important: split ext(insion) 就是用来划分文件扩展格式的,它返回的是一个元组，元组中的元素是文件名和'.扩展名'
            fpath=os.path.join(file_dir, safe_filename)
            async with aiofiles.open(fpath, 'wb') as f:
                while chunk := await file.read(1024*1024):
                    await file.write(chunk)
        else:
            not_allowed.append(file.filename)
            continue

    return {
        'msg':'success',
        'sum':len(files),
        'allowed':allowed,
        'allowed_sum':len(allowed),
        'not_allowed':not_allowed,
        'not_allowed_sum':len(not_allowed),
    }
"""
{
  "msg": "success",
  "sum": 4,
  "allowed": [
    "截图 2025-12-03 22-55-44.png",
    "截图 2025-12-03 16-35-12.png",
    "截图 2025-12-03 23-02-25.png"
  ],
  "allowed_sum": 3,
  "not_allowed": [
    "无标题-2025-10-18-1525.svg"
  ],
  "not_allowed_sum": 1
}
"""


'''
写入的时候发现会卡住一直等待，那么我们就需要一个解决方案
打开文件的时候也要异步处理
pip install aiofiles
然后改造with open 为 with aiofiles.open ,这样就让其支持异步
'''

# @Time    : 2025/12/18 10:00
# @Author  : hero
# @File    : 04拓展之pathlib.py


from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import os
import aiofiles
import uuid as uuidlib

app = FastAPI()


# 单个文件验证
@app.post('/download/')
async def download_file(file: UploadFile):
    suffix_allowd = ['.png', '.jpg', '.jpeg']
    downloaddir = './demopic'
    os.makedirs(downloaddir, exist_ok=True)
    file_suffix = Path(file.filename).suffix.lower() #important: 它会直接采集到'.'以及后面的内容
    if file_suffix in suffix_allowd:
        safe_filename = f"{uuidlib.uuid4().hex}{os.path.splitext(file.filename)[1]}"
        filepath = os.path.join(downloaddir, safe_filename)
        async with aiofiles.open(filepath, 'wb') as f:
            # 改造
            while chunk := await file.read(1024 * 1024):
                await f.write(chunk)

            return {
                'msg': 'success',
                'status': 200,
                'filename': file.filename
            }

    else:
        raise HTTPException(status_code=404, detail="File not allowed.")


# tips:限制上传格式
@app.post('/uploadpic_strict')
async def upload_pic_strict(files: list[UploadFile] = File(...)):
    file_dir = './demopic'
    os.makedirs(file_dir, exist_ok=True)
    # tips:定义限定后缀
    suffix_allowd = ['png', 'jpg', 'jpeg']
    # tips:定义允许列表,记录允许的文件
    allowed = []
    # tips:定义不被允许列表，记录不被允许的文件
    not_allowed = []
    for file in files:
        file_suffix = file.filename.split('.')[-1]
        if file_suffix in suffix_allowd:
            allowed.append(file.filename)  # tips:添加到允许列表中方便记录
            safe_filename = f"{uuidlib.uuid4().hex}{os.path.splitext(file.filename)[1]}"
            fpath = os.path.join(file_dir, safe_filename)
            async with aiofiles.open(fpath, 'wb') as f:
                while chunk := await file.read(1024 * 1024):
                    await file.write(chunk)
        else:
            not_allowed.append(file.filename)
            continue

    return {
        'msg': 'success',
        'sum': len(files),
        'allowed': allowed,
        'allowed_sum': len(allowed),
        'not_allowed': not_allowed,
        'not_allowed_sum': len(not_allowed),
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

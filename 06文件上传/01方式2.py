# @Time    : 2025/12/17 12:42
# @Author  : hero
# @File    : 01方式2.py
import os

from fastapi import FastAPI, UploadFile
import aiofiles
import uuid as uuidlib
app = FastAPI()


@app.post('/upload/')
async def upload_file(file: UploadFile):#tips:它是要比File方式更好的，因为它不用指定bytes类型，而且这样它就是一个在flask中学过的filestorge类型
    uploaddir = './demopic' #tips:创建上传文件夹
    if not os.path.exists(uploaddir):
        os.makedirs(uploaddir)
        filepath = os.path.join(uploaddir, file.filename)
        content=await file.read()
        with open(filepath, 'wb') as f:
            f.write(content)
    return {
        'file_name':file.filename,
        'file_size':file.size,
        'file':file
    }

@app.post('/download/')
async def download_file(file:UploadFile):
    downloaddir = './demopic'
    os.makedirs(downloaddir,exist_ok=True)
    safe_filename=f"{uuidlib.uuid4().hex}{os.path.splitext(file.filename)[1]}"
    filepath = os.path.join(downloaddir, safe_filename)
    # with open(filepath, 'wb') as f:
    #     f.write(await file.read())

    async with aiofiles.open(filepath, 'wb') as f:
        #改造
        while chunk:= await file.read(1024*1024):
            await f.write(chunk)

        return {
            'msg':'success',
            'status':200,
            'filename':file.filename
        }

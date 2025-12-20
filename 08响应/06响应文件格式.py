# @Time    : 2025/12/20 16:48
# @Author  : hero
# @File    : 06响应文件格式.py


import aiofiles
from fastapi import FastAPI
from fastapi.responses import Response, FileResponse, StreamingResponse  # tips：返回文件类型
from typing import Annotated

'''
文件响应是指fastapi在响应客户端请求时，返回一个文件内容的HTTP响应,通常包含文件的二进制数据或者文本数据
文件响应的关键特点 

内容类型:通过Content-Type头指定的MIME类型，如application/pdf(PDF文件)、text/csv (csv文件) 、application/vnd.ms-excel(Excel文件)

文件内容:响应的body包含文件的实际数据，可能是二进制或者文本
'''
app = FastAPI()


@app.get("/gettxtfile")
async def getfile():
    info = b'hello,i am  the  file content '  # tips:文本信息是以二进制的形式进行返回,所以要加上一个b
    # SyntaxError: bytes can only contain ASCII literal characters
    return Response(
        content=info,
        media_type="text/plain",  # tips:指定返回的是文本内容
        headers={
            "Content-Disposition": f"attachment; filename=hello.txt"  # tips:attachement代表的意思是i直接下载
        }
    )


# tips:再来一个返回pdf文件的接口,文件放在了demofile中 ,这时候我们可就不能用单纯Response了
@app.get('/getpdffile')
async def getpdffile():
    filepath = './demofile/尚硅谷高级技术之Shell.pdf'  # tips:注意，有中文名处理起来就会有大坑
    filename = filepath.split('/')[-1]

    return FileResponse(
        path=filepath,
        status_code=200,
        media_type="application/pdf",
        headers={
            # "Content-Disposition": f"attachment; filename={filename}"
            "Content-Disposition": "attachment; filename=demo.pdf}"
        }
    )


# tips:下载音频文件  ,我们采取StreamingResponse,或者也可以像上面那样直接用FileResponse
#  但是推荐StreamingResponse，因为它可以分段返回，譬如我们要下载一个无损音质的音乐，或者一部达到几个G的电影

# important:定义一个函数生成一个流
async def gen_stram_async(file_path: str, chunk_size: int = 1024 * 1024 * 10):  # tips指定chunk为默认1*10=10M
    async with aiofiles.open(file_path, 'rb') as f:
        while chunk := await f.read(chunk_size):
            yield chunk  # tips:用生成器一点点读，这样就避免了一次读大文件导致崩溃


@app.get('/downloadmp3')
async def downloadmp3():
    filepath = './demofile/demo.mp3'
    return StreamingResponse(
        content=gen_stram_async(filepath),
        status_code=200,
        media_type='video/m3',  # tips:指定的是mp3
        headers={
            'Content-Disposition': "attachment; filename=demo.mp3"
        }
    )

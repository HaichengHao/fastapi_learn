# @Time    : 2025/12/20 19:44
# @Author  : hero
# @File    : 07响应其它格式的数据.py

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

'''
本小节将会涉及到
字符串响应
重定向响应
html响应
静态文件响应
这些都不常用，了解即可
'''

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",  # React/Vue 默认端口
    "http://localhost:5173",  # Vite 默认端口
    "http://127.0.0.1:8099",  # 调试端口号
    # 添加你实际前端的地址
]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=['*'],  # tips:允许所有源
    allow_credentials=False,  # tips:如果允许所有源这里就得写False
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get_str")
async def get_str():
    return 'hello'


@app.get("/gethtml")
async def gethtml():
    # tips:如果直接返回不用HTMLResponse封装，返回的就是字符串的"<html><body><h1>hello</h1></body></html>" ，
    # 而不是<html><body><h1>hello</h1></body></html>
    return HTMLResponse(content="<html><body><h1>hello</h1></body></html>")


# tips:返回静态资源
app.mount("/static", StaticFiles(directory="static"), name="static")
# http://localhost:8099/static/截图 2025-12-03 16-33-10.png 这样访问就能访问

# tips:返回网页
app.mount("/templates", StaticFiles(directory="templates", html=True), name="templates")


# tips:重定向
@app.get('/get_redirect')
async def get_redirect():
    return RedirectResponse(url='https://www.bilibili.com/')

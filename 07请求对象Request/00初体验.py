# @Time    : 2025/12/18 10:49
# @Author  : hero
# @File    : 00初体验.py
from fastapi import FastAPI,Request

app = FastAPI()

@app.get('/')
async def index(request: Request):
    return {
        '请求url':request.url,
        '请求方法':request.method,
        '请求ip':request.client.host,
        '请求参数':request.query_params,
        '请求头':request.headers,
        '请求cookie':request.cookies,
        # '请求json':await request.json(),
        # '请求form':await request.form(),
        # '请求files':request.files,
        '请求路径参数':request.path_params
    }

"""
{
  "请求url": {
    "_url": "http://127.0.0.1:8099/"
  },
  "请求方法": "GET",
  "请求ip": "127.0.0.1",
  "请求参数": {},
  "请求头": {
    "host": "127.0.0.1:8099",
    "connection": "keep-alive",
    "sec-ch-ua-platform": "\"Linux\"",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    "accept": "application/json",
    "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "http://127.0.0.1:8099/docs",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
  },
  "请求cookie": {},
  "请求路径参数": {}
}"""
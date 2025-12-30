# @Time    : 2025/12/29 14:31
# @Author  : hero
# @File    : main.py
from urllib.request import Request

from fastapi import FastAPI,Response
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
origins=[
    "http://localhost",
    "http://localhost:65533",
    "http://localhost:63342"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, #tips:允许携带cookie
    allow_methods=['*'],
    allow_headers=["*"],

)

# @app.middleware('http')
# async def add_cors_header(request,call_next):
#     if request.method == "OPTIONS":
#         headers={
#             "Access-Control-Allow-Origin": "*",
#             "Access-Control-Allow-Methods": "*",
#             "Access-Control-Allow-Headers": "Content-Type,Authorization",
#             "Access-Control-Max-Age": "3600",
#
#         }
#         return Response(status_code=200,headers=headers)
#     response=await call_next(request)
#     return response


@app.get('/info')
async def index():
    return {'msg': 'hello world'}


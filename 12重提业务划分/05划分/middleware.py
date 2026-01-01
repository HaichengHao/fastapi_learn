# @Time    : 2026/1/1 22:26
# @Author  : hero
# @File    : middleware.py

from fastapi.middleware.cors import CORSMiddleware

def  add_cors_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

def request_middleware(app):
    @app.middleware('http')
    async def middleware(request,call_next):
        print('请求前')
        response = await call_next(request)
        print('请求后')
        return response
    return app
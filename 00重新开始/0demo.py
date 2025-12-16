from fastapi import FastAPI
import uvicorn
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello FastAPI! u the fastest python web framework"}


if __name__ == '__main__':
    uvicorn.run('0demo:app', host='127.0.0.1', port=8898, reload=True)
    #或者uvicorn.run(app, host='127.0.0.1', port=8898) 注意这样写不要指定reload参数

# uvicorn 0demo:app --host 127.0.0.1 --port 8099 --reload --log-level debug 或者通过命令来运行
# 或者进入开发版本服务器的fastapi dev 0demo.py 需要安装fastapi[standard]


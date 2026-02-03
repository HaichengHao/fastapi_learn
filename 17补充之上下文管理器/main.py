"""
@File    :main.py
@Editor  : 百年
@Date    :2026/2/9 16:58 
"""

from src import app
import uvicorn

if __name__ == '__main__':
    uvicorn.run(app,host='127.0.0.1',port=8080)



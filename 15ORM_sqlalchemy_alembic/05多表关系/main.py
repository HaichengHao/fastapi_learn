# @Time    : 2026/1/20 20:06
# @Author  : hero
# @File    : main.py

from fastapi import FastAPI,APIRouter
from views  import emp_apirt
app =  FastAPI()

app.include_router(emp_apirt,prefix='/api/v1')

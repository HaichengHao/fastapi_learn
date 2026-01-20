# @Time    : 2026/1/20 16:30
# @Author  : hero
# @File    : views.py
from http.client import HTTPException

from certifi import where
from fastapi import APIRouter,Path,Query,Body,Depends,HTTPException,status
from sqlalchemy import Select
from sqlalchemy.orm import Session
from typing import Annotated

from databases import get_session
from schemas import Empschema
from models import Employee

emp_apirt = APIRouter(prefix='/api/employee',tags=['员工管理'])

@emp_apirt.get('/')
async def getemp():
    pass

@emp_apirt.post('/emp/')
async def create_emp(employee:Empschema,session:Annotated[Session,Depends(get_session)]):
    #step1:先判断数据库中有没有重复的数据,即先进行查询
    is_emp =  session.execute(Select(Employee.name).where(Employee.name==employee.name))
    if is_emp: #tips:如果不为空,即已存在重复名字的员工
        raise HTTPException(status_code=405,detail='重复录入,已经存在该员工的信息')

    #tips:需要把Pydantic的模型对象(Empschema)转换为ORM的模型对象(Employee),
    #important:所以为了解决这个问题,我们刚才在定义Empschema的时候重写了Config将其设置为了from_attributes=True
    db_emp = Employee(**employee.model_dump()) #tips:这里和tortoiseorm差不多
    #tips:其实这里就跟curd操作当中创建员工对象的操作是一样的,就是新建一个员工对象然后**employee.model_dump()就是解包赋值

    session.add(db_emp)
    session.commit()  #important:之前我们使用的是sessionmaker来做的,所以会自动提交,但这次是我们手动管理session,所以需要提交



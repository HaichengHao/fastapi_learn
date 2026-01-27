# @Time    : 2026/1/20 16:30
# @Author  : hero
# @File    : views.py
from http.client import HTTPException
from fastapi import APIRouter, Depends, HTTPException,Query,Path,Body
from sqlalchemy import Select, update
from sqlalchemy.orm import Session
from typing import Annotated

from databases import get_session
from schemas import Empschema, DepartmentSchema, DetailEMPINFO
from models import Employee

emp_apirt = APIRouter(prefix='/employee', tags=['员工管理'])


# tips:根据传入的员工id返回详细的员工信息
@emp_apirt.get('/emp/{id}', response_model=DetailEMPINFO)
async def getemp(id:Annotated[int,Path(description='员工id')], session: Annotated[Session, Depends(get_session)]):
    result = session.get(Employee, id)
    if result:
        return result
    else:
        raise HTTPException(status_code=403, detail='未查讯到讯息')

#tips:分页查询员工信息

@emp_apirt.get('/emp',response_model=list[DetailEMPINFO],description='查询所有员工列表')
async def getall_emps(session: Annotated[Session, Depends(get_session)],offset:int=Query(title='输入的是offset',default=0),page_size:int=Query(default=5,description='每页最多显示的数量')):

    return session.scalars(Select(Employee).offset(offset).limit(page_size)).all()



# tips:新增员工
@emp_apirt.post('/emp/', description='添加员工', response_model=Empschema)
async def create_emp(emp: Empschema, session: Annotated[Session, Depends(get_session)]):
    # step1:先判断数据库中有没有重复的数据,即先进行查询
    is_emp = session.execute(Select(Employee.name).where(Employee.name == emp.name)).first()
    if is_emp:  # tips:如果不为空,即已存在重复名字的员工
        raise HTTPException(status_code=405, detail='重复录入,已经存在该员工的信息')

    # tips:需要把Pydantic的模型对象(Empschema)转换为ORM的模型对象(Employee),
    # important:所以为了解决这个问题,我们刚才在定义Empschema的时候重写了Config将其设置为了from_attributes=True
    db_emp = Employee(**emp.model_dump())
    # important:这里和tortoiseorm差不多,empl是pydantic类型,用.model_dump是转换成字典
    #  然后**emp.model_dump()就是解包赋值

    session.add(db_emp)
    session.commit()  # important:之前我们使用的是sessionmaker来做的,所以会自动提交,但这次是我们手动管理session,所以需要提交
    return db_emp


# tips:修改员工信息,通过id进行修改

@emp_apirt.put('/emp/{id}', response_model=Empschema)
async def mofy_emp(id:Annotated[int,Path(description='员工id')],session:Annotated[Session,Depends(get_session)],emp:Empschema):
    emp.id=id  #tips:因为不对id进行修改,所以这里直接先给其赋值
    target_emp = session.get(Employee,id)
    if target_emp==None:
        raise HTTPException(status_code=405,detail='未查讯到员工信息,请检查id')
    session.execute(update(Employee),[emp.model_dump(exclude_unset=True)])
    #important:这里不理解的话可以去看04session相关操作的笔记,model_dump()是把pydantic模型所有的属性转换为字典
    # 但是在做更新操作中可能某些属性并不用更新,如果不加上排除未设置属性,那么它将会修改我们并不需要更新的属性
    #tips:修改后要提交
    session.commit()

    #tips:然后返回修改后的数据方便查看结果
    db_emp = session.get(Employee,id)
    return db_emp


#tips:删除员工信息,通过id进行删除
@emp_apirt.delete('/emp/{id}')
async def  del_epm(id:Annotated[int,Path(description='员工id')],session:Annotated[Session,Depends(get_session)]):
    # session.delete(Employee,id)   #tips:物理删除,不推荐
    target_emp = session.get(Employee,id)
    if target_emp==None:
        raise HTTPException(status_code=405,detail='未查讯到员工信息,请检查id')
    session.execute(update(Employee).where(Employee.id == id).values(is_leave=1))
    session.commit()
    return {
        'id': target_emp.id,
        'msg':'删除成功'
    }

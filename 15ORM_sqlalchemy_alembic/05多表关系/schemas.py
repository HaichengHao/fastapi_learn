# @Time    : 2026/1/20 14:33
# @Author  : hero
# @File    : schemas.py
from decimal import Decimal
from datetime import date
from typing import Optional

from pydantic import BaseModel,Field
from models.employee import GenderValue
from  models.department import Department
class Empschema(BaseModel):
    id:int=Field(description='员工ID,添加数据的时候不用传递',default=None)
    name:str=Field(description='姓名')
    salary:Optional[float]=Field(description='薪资',default=None)
    bonus:int=Field(description='奖金',default=None)
    gender:GenderValue=Field(description='性别',default=GenderValue.MALE)
    is_leave:bool=Field(description='是否离职,True为离职',default=False) #默认不离职
    dep_id:Optional[int] = Field(description='员工所属部门id',default=None)
    entry_date:date=Field(description='入职时间',default=None)

    #important：这是关键,需要重写才可以实现sqlalchemy的模型和pydantic模型之间的转换
    class Config:
        from_attributes=True #important:有了这个配置才能把ORM模型转换为Pydantic模型对象



#tips:定义创建部门的schema,方便下面返回详细信息的时候调用此表的schema
class  DepartmentSchema(BaseModel):
    id:int=Field(description='员工部门的ID,添加数据的时候不要传',default=None)
    name:str=Field(description='部门名称',default=None)
    city:str=Field(description='部门所在城市的名称',default=None)

    class  Config:
        from_attributes=True

#tips：获取员工的详细信息,包含部门名称,只需要继承上面的Schema并新增一个部门名称即可,注意也要与employee表保持一致
# important:注意因为我们在employee表中定义的dep_name是属于Department类型的,所以这里也得是Department类型

class DetailEMPINFO(Empschema):
    '''
    响应员工信息的模型类,包含该员工的所属部门
    '''
    dep_name:Optional[DepartmentSchema]= Field(description='所属部门',default=None)
    class Config:
        from_attributes=True



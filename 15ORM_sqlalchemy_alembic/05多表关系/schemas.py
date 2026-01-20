# @Time    : 2026/1/20 14:33
# @Author  : hero
# @File    : schemas.py
from decimal import Decimal
from datetime import date
from pydantic import BaseModel,Field
from models.employee import GenderValue

class Empschema(BaseModel):
    id:int=Field(description='员工ID,添加数据的时候不用传递')
    name:str=Field(description='姓名')
    salary:Decimal=Field(description='薪资',default=None)
    bonus:int=Field(description='奖金',default=None)
    gender:GenderValue=Field(description='性别')
    is_leave:bool=Field(description='是否离职,True为离职',default=False) #默认不离职
    dep_id:int = Field(description='员工所属部门id',default=None)
    entry_date:date=Field(description='入职时间',default=None)

    #important：这是关键,需要重写才可以实现sqlalchemy的模型和pydantic模型之间的转换
    class Config:
        from_attributes=True



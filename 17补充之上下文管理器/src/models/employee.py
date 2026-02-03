"""
@File    :employee.py
@Editor  : 百年
@Date    :2026/2/9 18:57 
"""
from sqlalchemy import DateTime, func,String,DECIMAL,Boolean,Enum as SAEnum,\
    or_,ForeignKey
import enum
from . import Base

from typing import Optional
from datetime import datetime,date
from sqlalchemy.orm import mapped_column,Mapped,relationship
from decimal import Decimal
class TimestampMixin:
    created_time:Mapped[datetime]=mapped_column(
        DateTime,
        insert_default=func.now(),
        comment='创建时间'

    )
    update_time:Mapped[datetime]=mapped_column(
        DateTime,
        insert_default=func.now(),
        onupdate=func.now(),
        comment='记录修改时间'
    )
class GenderValue(enum.Enum):
    MALE = '男'
    FEMAL='女'
class Employee(Base,TimestampMixin):
    __tablename__ = 'employee'
    id:Mapped[int]=mapped_column(primary_key=True,autoincrement=True)
    name:Mapped[str]=mapped_column(String(40),unique=True,nullable=False)
    salary:Mapped[Decimal]=mapped_column(DECIMAL(10,2),nullable=False)
    bonus:Mapped[int]=mapped_column(default=0,comment='员工资金')
    is_leave:Mapped[int]=mapped_column(Boolean,default=False,comment='是否离职，默认为非')
    gender:Mapped[GenderValue]=mapped_column(SAEnum(GenderValue),nullable=False)
    entry_date:Mapped[date]=mapped_column(DateTime,insert_default=func.now(),nullable=False,comment='入职时间')


# @Time    : 2026/1/12 13:43
# @Author  : hero
# @File    : employee.py

import enum
from  .  import Base
from typing import Optional
from datetime import datetime,date
from decimal  import Decimal
from sqlalchemy.orm import DeclarativeBase, sessionmaker, create_session, Mapped, mapped_column, relationship

from sqlalchemy import create_engine, DateTime, func, String, DECIMAL, Integer, Boolean, select, text, Enum as SAEnum, \
    or_, ForeignKey


# ✅ 2. 公共字段用 Mixin 类
class TimestampMixin:
    create_time: Mapped[datetime] = mapped_column(
        DateTime,
        insert_default=func.now(),
        comment='记录创建的时间'
    )
    update_time: Mapped[datetime] = mapped_column(
        DateTime,
        insert_default=func.now(),
        onupdate=func.now(),
        comment='记录修改时间'
    )


class GenderValue(enum.Enum):
    '''通过枚举设置字段'''
    MALE = '男'
    FEMALE = '女'


# tips:这是sqlalchemy写法，其实可以用sqlmodel的写法也可以
class Employee(Base, TimestampMixin):
    __tablename__ = 'employee'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    salary: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False, comment='员工薪资')
    bonus: Mapped[int] = mapped_column(default=0, comment='员工奖金')
    is_leave: Mapped[bool] = mapped_column(Boolean, default=False, comment="员工是否离职，默认不离职")
    gender: Mapped[GenderValue] = mapped_column(SAEnum(GenderValue), nullable=False)  # tips:利用枚举类来自动匹配
    entry_date: Mapped[date] = mapped_column(DateTime, insert_default=func.now(), nullable=False, comment='入职时间')

    #tips:设置一个外键位,因为一个部门有多个员工
    dep_id:Mapped[int]=mapped_column(ForeignKey('department.id'),nullable=False,)
    #tips:员工类中也要关联属性
    # 定义一个关联属性：该员工所处的部门,一个员工对应一个部门,所以其类型
    dep_name: Mapped[Optional['Department']] = relationship('Department',back_populates='emp_lst')
    def __str__(self):
        return f'{self.name},{self.salary},{self.bonus},{self.gender}'

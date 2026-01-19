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
    dep_id:Mapped[Optional[int]]=mapped_column(ForeignKey('department.id'))
    #tips:员工类中也要关联属性
    # 定义一个关联属性：该员工所处的部门,一个员工对应一个部门,所以其类型写的也是Department类型的,不过要指定其可选，避免污染已有数据
    dep_name: Mapped[Optional['Department']] = relationship(back_populates='emp_lst')

    #tips:添加关联关系,主表不用写single_paret
    idc:Mapped[Optional['IDCard']]=relationship( back_populates='emp')

    def __str__(self):
        return f'{self.name},{self.salary},{self.bonus},{self.gender}'


class  IDCard(Base):
    __tablename__ = 'id_card'
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    card_number:Mapped[str]=mapped_column(String(18),unique=True,nullable=False,comment='身份证号码')

    native_place:Mapped[Optional[str]]=mapped_column(String(40),nullable=True,comment='籍贯信息')

    #tips:添加外键约束,由于是一对一关联关系,所以在emp表或者idc表添加都可以
    emp_id :Mapped[int] = mapped_column(ForeignKey('employee.id'))
    #tips:设置关联属性,设置single_parent表示一个从表只能关联一个主表的记录,譬如一个身份证只能对应一名员工,不能一个身份证对应多个员工
    emp:Mapped[Optional['Employee']] = relationship(single_parent=True,back_populates='idc')
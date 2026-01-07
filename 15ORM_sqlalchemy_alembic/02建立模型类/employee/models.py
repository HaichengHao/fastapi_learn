# @Time    : 2026/1/6 17:33
# @Author  : hero
# @File    : models.py
import enum
from datetime import datetime
from decimal import Decimal



from db_main   import engine
# from ..db_main import Base# tips:from sqlalchemy.orm import DeclarativeBase as Base 不想用自己修改的Base的话就引入这个直接
from sqlalchemy.orm import Mapped,mapped_column,DeclarativeBase
from sqlalchemy import create_engine,DateTime,func,String,DECIMAL,Boolean,Enum as SAEnum
from sqlmodel import SQLModel,Field





# ✅ 1. 纯净的 Base（不包含任何字段！）
class Base(DeclarativeBase):
    pass  # ← 必须为空！


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


#tips:这是sqlalchemy写法，其实可以用sqlmodel的写法也可以
class Employee(Base,TimestampMixin):
    __tablename__ = 'employee'
    id:Mapped[int]=mapped_column(primary_key=True,autoincrement=True)
    name:Mapped[str]=mapped_column(String(40),unique=True,nullable=False)
    salary:Mapped[Decimal]=mapped_column(DECIMAL(10,2),nullable=False,comment='员工薪资')
    bonus:Mapped[int]=mapped_column(default=0,comment='员工奖金')
    is_leave:Mapped[bool]=mapped_column(Boolean,default=False,comment="员工是否离职，默认不离职")
    gender:Mapped[GenderValue]=mapped_column(SAEnum(GenderValue),nullable=False) #tips:利用枚举类来自动匹配





#tips:或者这种写法,更加清晰明了
# class User(SQLModel,table=True):
#     uid:int=Field(primary_key=True)
#     name:str=Field(nullable=False)
#     time_:datetime=Field(default=datetime.now)



#tips:先学会阻塞同步
if __name__ == '__main__':
    Base.metadata.create_all(engine)#tips:利用这个来创建表
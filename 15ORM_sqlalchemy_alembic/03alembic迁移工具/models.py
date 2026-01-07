# @Time    : 2026/1/7 09:30
# @Author  : hero
# @File    : models.py
import enum
from datetime import datetime, date
from decimal import Decimal
from unicodedata import name

from sqlalchemy.dialects.mysql import insert
# from db_main   import engine
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, sessionmaker
from sqlalchemy.engine import create_engine
from sqlalchemy import create_engine, DateTime, func, String, DECIMAL, Enum as SAEnum, Boolean
from sqlmodel import SQLModel, Field

engine = create_engine(
    url='mysql+pymysql://niko:HHCzio20@localhost:3306/fastapidb4',
    echo=True
)


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


if __name__ == '__main__':
    with sessionmaker(engine).begin() as session:
        # tips:新增数据
        # emp1 = Employee(
        #     name='张三',
        #     salary=2000,
        #     bonus=300,
        #     gender=GenderValue.MALE,
        #     entry_date=date(2026, 1, 7),
        # )
        emp2 = Employee(
            name='李四',
            salary=5000,
            bonus=300,
            gender=GenderValue.FEMALE,
            entry_date=date(2026, 1, 8),
        )
        emp3 = Employee(
            name='王五',
            salary=3000,
            bonus=3000,
            gender=GenderValue.FEMALE,
            entry_date=date(2026, 1, 9),
        )
        # session.add(emp1)
        #tips:批量添加
        session.add_all([emp2,emp3])

        #tips:方式2,类sql方式，了解为主
        inert_stmt=insert(Employee).values(name='陈六',salary=5000,bonus=300,gender=GenderValue.FEMALE,entry_date=date(2026, 1, 9))

        batchdata=[{'name':'刘七','salary':800,'bonus':1000,'gender':GenderValue.MALE,'enntry_data':datetime(2026, 1, 9)},
                   {'name':'刘八','salary':1800,'bonus':1000,'gender':GenderValue.MALE,'enntry_data':datetime(2026, 1, 9)}]
        inert_stmt=insert(Employee).values(name='陈六',salary=5000,bonus=300,gender=GenderValue.FEMALE,entry_date=date(2026, 1, 9))
        insertbatchdata = insert(Employee)
        session.execute(inert_stmt)
        session.execute(insertbatchdata,batchdata)
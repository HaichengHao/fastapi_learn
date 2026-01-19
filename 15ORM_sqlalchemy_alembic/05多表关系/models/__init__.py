# @Time    : 2026/1/12 13:37
# @Author  : hero
# @File    : __init__.py.py


from sqlalchemy.orm import DeclarativeBase,sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import *
from datetime import date

#
engine = create_engine(
    url='mysql+pymysql://niko:HHCzio20@localhost:3306/fastapidb4',
    echo=False
)

class Base(DeclarativeBase):
    pass
#
#
# ✅ 关键：显式导入所有模型，触发类注册到 Base.metadata
from .employee import Employee,GenderValue,IDCard
from .department import Department

# （可选）导出方便使用
__all__ = ["Base", "Employee", "Department"]
#
#
# if __name__ == '__main__':
#     with sessionmaker(bind=engine) as session:
#
#         #tips:增加部门
#         dep1 = Department(
#             name='六必居',
#             city='北京',
#
#         )
#         session.add(dep1)
#
#         emp1 = Employee(
#             name='张三',
#             salary=2000,
#             bonus=300,
#             gender=GenderValue.MALE,
#             entry_date=date(2026, 1, 7),
#         )
#         emp2 = Employee(
#             name='李四',
#             salary=5000,
#             bonus=300,
#             gender=GenderValue.FEMALE,
#             entry_date=date(2026, 1, 8),
#         )
#         #tips:给员工指定部门,按照我们刚才搞的指定关联关系来指定
#         # emp1.dep_name=dep1
#         # emp2.dep_name=dep1
#         #tips:也可以站在部门表的视角
#         dep1.emp_lst=[emp1,emp2]
#
#
#         session.add(dep1) #important:由于建立了关联关系,如果我们执行添加的话,部门表和员工表就都有了
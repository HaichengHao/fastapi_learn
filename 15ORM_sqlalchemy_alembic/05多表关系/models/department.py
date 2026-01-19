# @Time    : 2026/1/12 13:48
# @Author  : hero
# @File    : department.py

from  typing import Optional

from . import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey


class Department(Base):
    __tablename__ = 'department'
    id :Mapped[int] = mapped_column(primary_key=True
                                     ,autoincrement=True)

    name:Mapped[str]=mapped_column(String(40),name='dname',unique=True,nullable=False)
    city:Mapped[Optional[str]]=mapped_column(String(40)) #可以为空

    #important:定义关联属性,一个部门有多个员工,所以外键设置在员工表中，这边设置relationship,和之前学flask的时候很像
    # 双向关系不是必须的,但是在某些情况下会非常方便，譬如我们可以用员工表来回调查询部门表获取员工对应的部门表中的详细信息

    #tips:一个部门下的所有员工,由于其已经不是一个字段而是一个集合了，所以不能用column来对应单个字段了
    # back_populates:回调属性，或者说是关联属性,就很像flask中的backref
    # emp_lst:Mapped[list['Employee']]  =  relationship('Employee',back_populates='dep_name')

    #important:“本部门（Department 实例）可以通过 emp_lst 属性访问它所有的员工（Employee 对象列表）。
    # 而每个员工对象内部，有一个叫 dep_name 的属性，可以反向指回这个部门。”
    emp_lst:Mapped[list['Employee']]  =  relationship(back_populates='dep_name')


    #tips:实现自关联
    #tips:定义一个外键pid,关联到父机构id
    pid:Mapped[Optional[int]]=mapped_column(ForeignKey('department.id'),nullable=True) #自己关联自己,所以外键就是自己的主键,允许为空，因为顶级机构没有父机构

    #tips:定义关联属性
    # 当前机构的所有子机构列表
    children:Mapped[list['Department']] = relationship(back_populates='parentname')
    # 当前机构的父机构
    parentname:Mapped[Optional['Department']] = relationship(back_populates='children',remote_side=[id]) #important:自关联的时候一定要加上

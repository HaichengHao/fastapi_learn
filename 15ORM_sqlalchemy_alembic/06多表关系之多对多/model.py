# @Time    : 2026/1/14 16:30
# @Author  : hero
# @File    : model.py
from typing import Optional

from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import *

engine = create_engine('mysql+pymysql://niko:HHCzio20@localhost:3306/fastapidb5')


class Base(DeclarativeBase):
    __abstract__ = True


# important:定义中间表,它是一个纯粹的表
midtable = Table(
    'userandrole',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('role.id'), primary_key=True),
)


class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, comment='用户名')
    password: Mapped[str] = mapped_column(String(20), nullable=False, comment='密码')
    # tips:构建多对多的关联关系
    roles: Mapped[Optional[list['Role']]] = relationship(secondary=midtable,
                                                         back_populates='users')  # tips:学下来发现,sqlalchemy用在fastapi中和flask的写法是差不多的,尤其是涉及到多表关系


class Role(Base):
    __tablename__ = 'role'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False, comment='角色名')
    users: Mapped[Optional[list['User']]] = relationship(secondary=midtable, back_populates='roles')


if __name__ == '__main__':
    with sessionmaker(bind=engine).begin() as session:
        # important:多对多的数据操作
        u1 = User(username='zhangsan',password='zhangsan123')
        u2 = User(username='lisi',password='lisi123')

        r1 = Role(name='仓库管理员')
        r2 = Role(name='系统管理员')

        #tips:给u1指定两个角色
        u1.roles.append([r1,r2])
        u2.roles=[r2]
        session.add(u1)
        #important:这样添加一个就会找到u1关联了r1和r2,然后添加r2的时候发现r2和u2有关联关系,也会自动添加

        user = session.get(User,1)
        print(user.role[0].name)
        print(user.role[1].name)
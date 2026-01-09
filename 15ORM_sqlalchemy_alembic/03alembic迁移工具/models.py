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
from sqlalchemy import create_engine, DateTime, func, String, DECIMAL, Enum as SAEnum, Boolean, select, text, update, \
    delete, and_, or_
from sqlmodel import SQLModel, Field

engine = create_engine(
    url='mysql+pymysql://niko:HHCzio20@localhost:3306/fastapidb4',
    echo=False
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
    def __str__(self):
        return f'{self.name},{self.salary},{self.bonus},{self.gender}'

if __name__ == '__main__':
    with sessionmaker(engine).begin() as session:

        #important：增加操作
        '''
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
        
        '''

        #important：查询操作

        #tips:根据主键查询
        targetemp = session.get(Employee,2)
        print(targetemp)
        print(targetemp.name,targetemp.salary)

        #tips:查询所有数据
        sqlstat  = select(Employee)
        allemply = session.scalars(sqlstat) #important:scalars()返回的是模型类对象
        print(allemply)
        for emp in allemply:
            print(emp)

        #tips:返回指定字段的数据
        sqlstat2= select(Employee.name,Employee.salary)
        res = session.execute(sqlstat2)
        for emp in res:
            print(emp.name,emp.salary) #tips:打印对应的属性名
        # print(res)

        #tips:原生sql写法
        sql = text('select id,name,salary from employee')
        resalt = session.execute(sql).all()
        for obj in resalt:
            print(obj)
            print(obj.name,obj.salary)


        #otway:另外一种写法,执行语句不变但是返回的是模型类对象,理解即可
        sql = text('select id,name,salary from employee')
        #tips:建立映射关系
        orm_map = sql.columns(Employee.id,Employee.name,Employee.salary)
        statment = select(Employee).from_statement(sql)
        res = session.execute(statment).scalars()
        for obj in res:
            print(type(obj))
            print(obj)
            # print(obj.id,obj.name,obj.salary)


        #important:修改操作

        #tips:
        #先查询后修改,譬如按照主键查询到id为1的修改其名字
        # employee1 = session.get(Employee,1)
        #接着对其进行修改操作
        # employee1.name  = '张一'
        #tips:这样就可以了，不用像之前tortoiseORM那样需要save

        #tips:优化型
        # stmt = update(Employee).where(Employee.id == 2).values(name='kaven',salary=2000)
        # session.execute(stmt)


        #tips:批量修改
        # session.execute(update(Employee),[
        #     {'id':1,'bonus':600},
        #     {'id':3,'bonus':11600,'name':'niko'}
        # ])

        #important:删除操作，物理删除
        #第一种方式
        # emp = session.get(Employee,3)
        # session.delete(emp)
        #
        # #第二种方式
        # stmt = delete(Employee).where(Employee.id == 3)
        # session.execute(stmt)
        #

        #第三种方式，直接用sql
        # statment2 = text('delete from employee where id = 3')
        # session.execute(statment2)



        #important：高级查询

        stmt = select(Employee).where(Employee.name.like('%四%'),Employee.salary>2000)
        #多条件组合
        # stmt2 = select(Employee).where(and_(Employee.name.like('%四%'),Employee.salary>2000))
        res_lst = session.execute(stmt).scalars()
        for obj in res_lst:
            print('查询结果',obj)
        # print(res)

        #tips:找到不姓张的
        # stmt3 = select(Employee).where(Employee.name.regexp_match(r'^[^张]'))
        stmt4 = select(Employee).where(~Employee.name.startswith('张'))
        res_lst2 = session.execute(stmt4).scalars()
        for obj in res_lst2:
            print(obj)

        #tips:找到id是1,和id是5的
        # stmt5 = select(Employee).where(Employee.id.in_([1,5]))
        stmt5 = select(Employee).where(or_(Employee.id==1,Employee.id==5))
        result = session.execute(stmt5).scalars()
        for obj in result:
            print('---',obj)


        #tips:聚合函数，取出薪资平均值
        avgsalary = session.execute(select(func.avg(Employee.salary))).scalar()
        print(avgsalary)

        #tips:sql写法
        sql2 = text('select avg(salary) from employee')
        res = session.execute(sql2).scalar()
        print('平均工资',res)


        #tips:统计总人数
        empsum  = session.execute(select(func.count(Employee.id))).scalar()
        print(empsum)

        #tips:统计最小工资
        minsa = session.execute(select(func.min(Employee.salary))).scalar()
        print(minsa)
        #统计最小工资的员工姓名


        #tips:先用子查询查到最小工资，再进行判断看哪个工资等于这个工资
        minsalary = session.execute(select(func.min(Employee.salary))).scalar()

        minsae = session.execute(select(Employee.name).where(Employee.salary == minsalary)).scalar()
        print(minsae)
        #但是!!!⚠️这样是有歧义的,因为可能很多个员工的工资都是这样的,所以最好是用scalars().all()找到所有的
        minsaes  = session.execute(select(Employee.name).where(Employee.salary==minsalary)).scalars().all()
        print(minsaes)

        #otway：用排序来检索
        stmt = select(Employee.name).order_by(Employee.salary).limit(1)
        name = session.execute(stmt).scalar()  # 取第一个
        print("最低工资的员工（之一）:", name)


        #tips:查询工资第一高的
        hsa = session.execute(select(func.max(Employee.salary))).scalar()
        hieste = session.execute(select(Employee.name).where(Employee.salary==hsa)).scalars().all()
        print(hieste)


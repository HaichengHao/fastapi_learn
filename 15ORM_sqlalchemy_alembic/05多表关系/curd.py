# @Time    : 2026/1/14 09:40
# @Author  : hero
# @File    : curd.py

from models.employee import Employee, GenderValue,IDCard
from models.department import Department
from sqlalchemy import *
from datetime import date
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    url='mysql+pymysql://niko:HHCzio20@localhost:3306/fastapidb4',
    echo=False
)

if __name__ == '__main__':
    with sessionmaker(engine).begin() as session:
        #tips:给id为1的员工绑定身份证号码
        # idc = IDCard(card_number='103387200011110666',native_place='北京',emp_id=1)
        # session.add(idc)

        #tips:通过员工表查询其身份证号码
        EMP1= session.get(Employee,1)
        print(EMP1.idc.card_number)
        '''
        # dep1 = Department(name='深圳总公司', city='深圳')  #tips:创立总公司记录
        # session.add(dep1)

        dep0 = Department(name='行政部',city='深圳',pid=1)
        dep2 = Department(name='郑州二七区分公司',city='郑州',pid=1) #tips:指定pid,表明其母公司id为1,实现department表的自关联
        dep3 = Department(name='销售部',parentname=dep2,city='郑州') #tips:指定其为郑州分公司的部门

        session.add(dep0)
        session.add(dep2) #tips:这样只需要单独添加dep2,则与其有关联关系praentname的子节点dep3也会被创建
        '''
        '''
         # tips:增加部门
         dep1 = Department(
             name='六必居',
             city='北京',
 
         )
 
         dep2 = Department(
             name='蜜雪冰城',
             city='郑州'
         )
 
         # session.add(dep1)
         session.add(dep2)
         emp1 = Employee(
             name='张三',
             salary=2000,
             bonus=300,
             gender=GenderValue.MALE,
             entry_date=date(2026, 1, 7),
         )
         emp2 = Employee(
             name='李四',
             salary=5000,
             bonus=300,
             gender=GenderValue.FEMALE,
             entry_date=date(2026, 1, 8),
         )
 
         emp3 = Employee(
             name='王五',
             salary=4000,
             bonus=3000,
             gender=GenderValue.FEMALE,
             entry_date=date(2026, 1, 9),
         )
         # tips:给员工指定部门,按照我们刚才搞的指定关联关系来指定
         # emp1.dep_name=dep1
         # emp2.dep_name=dep1
         # tips:也可以站在部门表的视角
         # dep1.emp_lst = [emp1, emp2]
         dep2.emp_lst = [emp3]
 
         # session.add(dep1) #important:由于建立了关联关系,如果我们执行添加的话,部门表和员工表就都有了
         session.add(dep2)
         '''

        # important:修改操作,先查后改
        '''
        emp2   = session.get(Employee,2)
        dept = session.get(Department,2)
        emp2.dep_name = dept #tips:通过关联属性来关联
        emp2.dep_id = dept.id #tips:通过外键来关联
        #tips:也可以站在部门视角
        # dept.emp_lst = [emp2]
        
        ustmt = Update(Employee).where(Employee.name=='张三').values(salary=2123)
        session.execute(ustmt)
        '''

    # important:查询操作

    '''
     #tips:通过部门表查询员工
     dept = session.get(Department,1)
     employeeslst = dept.emp_lst
     for emp in employeeslst:
         print(emp)
     #tips:通过员工表来查询部门,通过关联关系来查找,因为关联的dep_name的类型是Department大类,所以要想拿到大类里的属性就得通过大象类型,拿到它的.name
     emp2  = session.get(Employee,2)
     print(emp2.dep_name.name)

     #important:删除操作
     #tips:设置张三的部门为空
     session.execute(Update(Employee).where(Employee.name=='张三').values(dep_id=None))

     #tips:或者先查后删除
     emplisi = session.get(Employee,2)
     emplisi.dep_id = None
 '''





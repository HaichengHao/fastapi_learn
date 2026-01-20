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



        # important:关联复杂查询

        # 查询2026年入职的员工名以及该员工所在的部门名称
        # extract就是我们想要抽取的内容,我们利用extract从Employee表的entry_date字段中抽取出年份
        stmt = Select(Employee.name, Department.name).join(Department).where(
            extract('year', Employee.entry_date) == 2026)
        result = session.execute(stmt)
        for row in result:
            print(row.name, row.name_1)

        #tips:或者我们还有别的解决方案,利用别名方式来更方便取值
        stmt2 = Select(Employee.name.label('ename'),Department.name.label('dname')).join(Department,isouter=True).where(extract('year', Employee.entry_date) == 2026)
        res   = session.execute(stmt2)
        for row in res:
            print(row.ename, row.dname)


        #tips:查询身份号码是103387200011110666的员工姓名以及其所属部门
        stmt3 = Select(Employee.name.label('ename'),Department.name.label('dname')).join(IDCard).join(Department,isouter=True).where(IDCard.card_number == "103387200011110666")
        res = session.execute(stmt3)
        for row in res:
            print(row.ename, row.dname)


        #tips:查询每个部门的名字以及部门下的员工个数

        #语句思路:选择外连接,
        stmt4 = Select(Department.name.label('dname'),func.count(Employee.id).label('ecount')).join(Employee,isouter=True).group_by(Department.id)
        res = session.execute(stmt4)
        for row in res:
            print(row.dname,row.ecount)

        #tips:查询每个部门的名字,city以及部门下的员工个数
        #可以去department.py中改写表的__str__返回
        stmt5 = Select(Department,func.count(Employee.id).label('ecount')).join(Employee,isouter=True).group_by(Department.id)
        res = session.execute(stmt5)
        for row in res:
            print(row[0],row[1])


        #tips:查询每个部门的名字以及它里面的员工数量,并且按照员工数量的个数降低序排序
        stmt6 = Select(Department.name,func.count(Employee.id).label('ecount')).join(Employee,isouter=True).group_by(Department.id).order_by(desc('emp_count'))
        res = session.execute(stmt6)
        for row in res:
            print(row[0],row[1])
        #important:一对一操作RUD
        '''
        #tips:给id为1的员工绑定身份证号码
        # idc = IDCard(card_number='103387200011110666',native_place='北京',emp_id=1)
        # session.add(idc)

        #tips:通过员工表查询其身份证号码
        EMP1= session.get(Employee,1)
        print(EMP1.idc.card_number)  #important:因为其是一对一关联关系,而且EMP1是一个Employee对象,根据大象类型,其对应的.idc其实是IDCard对象,然后我们利用了这个拿到了它的属性card_number
        '''


        #important:crud
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




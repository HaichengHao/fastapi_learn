# @Time    : 2025/12/22 13:21
# @Author  : hero
# @File    : 脚本模式.py


from tortoise import Tortoise,run_async
from  usermodel import Student

#important 定义数据增加函数
async def create_student(name:str,age:int=None,email:str=None):
   stu= await Student.create(name=name,age=age,email=email)#tips:因为是异步操作，所以前面要加上await

   return stu

#tips:定义数据删除函数
async def del_student(name:str):
    stu=await Student.filter(name=name).first()
    if not stu:
        return False
    await stu.delete()
    return True

#tips：定义数据修改函数
async def update_student(id:int,name:str=None,age:int=None,email:str=None):
    stu=await Student.get(id=id)
    if not stu:
        return False
    else:
        if name:
            stu.name=name
        if age:
            stu.age=age
        if email:
            stu.email=email
        stu.save()
        return True

#tips:获取单条数据
async def get_stu(id:int)->Student:
    stu = await Student.get(id=id)
    return stu

#tips:获取多条数据
async def get_manystu(name:str)->list[Student]:
    manystu=await Student.filter(name=name).all()
    return manystu
#tips:获取所有数据
async def get_allstu()->list[Student]:
    allstu  = await Student.all()
    return allstu


#tips:模糊查询
async def get_student(name:str):
    stu=await Student.filter(name__contains=name)
    return stu
#tips:多条件模糊查询
async def get_allstudent(name:str,age:int)->list[Student]:
    stu=await Student.filter(name__contains=name,age=age).all()
    return stu


async def init():
    await Tortoise.init(  #tips:定义数据库连接初始化方法，告诉程序我们要连哪个数据库，用哪个表(model)
        db_url='mysql://niko:HHCzio20@localhost:3306/fastapidb',
        modules={
            'models': ['usermodel'] #tips:注意这里如果是单项目的话就u不用写app.usermodel
        }
    )

async def main():
    await init() #tips:先运行初始化数据库连接
    #tips:再添加数据
    stu1=await create_student(
        name='张三',
        age=18,
        email='zhangsan@qq.com'
    )
    print(f'创建成功{stu1.name},{stu1.email}')
    stu2=await create_student(
        name='李四',
        age=21,
        email='lisi@qq.com'
    )
    print(f'创建成功{stu2.name},{stu2.email}')

    stu3=await create_student(
        name='王五',
        age=22,
        email='wangwu@qq.com' #tips:这里写是为了测试唯一约束
    )
    print(f'创建成功{stu3.name},{stu3.email}')

    allstu=await get_allstu() #tips:获取所有
    manystu=await get_manystu(name='王三') #tips:获取多条
    stu = await get_stu(id=1)#tips:获取指定id对应的单条数据
    somestu=await get_student(name='王') #tips:模糊查询


if __name__ == '__main__':
    run_async(main()) #tips:因为是异步的，所以要用异步的执行方式

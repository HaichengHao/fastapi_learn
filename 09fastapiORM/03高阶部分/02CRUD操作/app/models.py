# @Time    : 2025/12/26 12:32
# @Author  : hero
# @File    : models.py

import datetime
import re
from tortoise import fields,Tortoise,run_async
from tortoise.models import Model


def agevalidator(value: int):
    if value > 100 | value < 0:
        raise ValueError('输入年龄信息有误')
    else:
        return value
def phonevalidator(value: str):
    if re.match(r'^1[3-9]\d{9}$', value):
        return value
    else:
        raise ValueError('手机号格式有问题')
#tips:学生表
class Student(Model):
    stuid:int=fields.IntField(pk=True)
    name:str=fields.CharField(max_length=50)
    age:int=fields.IntField(validators=[agevalidator,])
    profile:str=fields.OneToOneField('models.StudentProfile',on_delete=fields.CASCADE,related_name='student',null=True)
    #tips:related_name表示反向查询引用标识，譬如知道档案想要查询学生表的时候就可以通过它来查到，和flask中的backref一样的，
    # 如StudentProfile对象.student.name,这样就可以通过档案表找到学生信息
    #

#tips:学生档案表
class StudentProfile(Model):
    pfid:int=fields.IntField(pk=True)
    address:str=fields.CharField(max_length=50) #档案保存地址
    phonenum:str=fields.IntField(validators=[phonevalidator])

#多对多关系
#tips:课程表
class Course(Model):
    cid:int=fields.IntField(pk=True)
    cname:str=fields.CharField(max_length=50)
    #tips:或者像django一样
    # students = fields.ManyToManyField('models.Student',related_name='courses',through='StudentCourse')

# #tips：学生课程关系表
class StudentCourse(Model):
    id:int=fields.IntField(pk=True)
    #tips:如果不懈relarted_name的话默认也是链到外键表的主键
    course_id:int=fields.ForeignKeyField('models.Course',on_delete=fields.CASCADE) #tips:这里就和django很像！
    student_id:int=fields.ForeignKeyField('models.Student',on_delete=fields.CASCADE)
    class Meta:
        unique_together=(('course_id','student_id'),)  #tips:约束可以有多个，被元组包裹，所以最好这样写不容易忘


#
# #tips:成绩表
class Score(Model):
    sid:int=fields.IntField(pk=True)
    date:datetime=fields.DatetimeField(auto_now_add=True)
    score:float=fields.FloatField()
    stuid:int=fields.ForeignKeyField('models.Student',on_delete=fields.CASCADE,related_name='score')



#tips:测试脚本方式
# async def  init():
#     await Tortoise.init(
#         db_url='mysql://niko:HHCzio20@localhost:3306/fastapidb1',
#         modules={
#             "models":['models']
#         }
#     )
#     await Tortoise.generate_schemas() #important:注意这里必须加上,不加上表就不会生成,但是如果是复用的话这行就必须去掉
#
# if __name__ == '__main__':
#     run_async(init())
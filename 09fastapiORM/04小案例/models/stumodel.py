# @Time    : 2025/12/29 09:44
# @Author  : hero
# @File    : stumodel.py

from tortoise.models import Model
from tortoise import fields

def agevalidator(value):
    if value > 18:
        return value
    elif value < 0:
        raise ValueError('年龄不能为负数')


class  Student(Model):
    id=fields.IntField(pk=True)
    name=fields.CharField(max_length=100)
    age=fields.IntField(null=False,validators=[agevalidator])
    pwd=fields.CharField(max_length=100,description='密码')
    sno=fields.IntField(description='学号')
    clas = fields.ForeignKeyField('models.Clas',related_name='students')

class Teacher(Model):
    id=fields.IntField(pk=True)
    name=fields.CharField(max_length=100)
    pwd=fields.CharField(max_length=100)
    tno=fields.IntField(description='老师编号')

class Course(Model):
    id=fields.IntField(pk=True)
    name=fields.CharField(max_length=100,description='课程名')
    teacher=fields.ForeignKeyField('models.Teacher',related_name='courses')

class  Coursestu(Model):
    id=fields.IntField(pk=True)
    stu=fields.ForeignKeyField('models.Student',related_name='courstu')
    course=fields.ForeignKeyField('models.Course',related_name='courstu')


class  Clas(Model):
    id=fields.IntField(pk=True)
    name=fields.CharField(max_length=100,description='班级')
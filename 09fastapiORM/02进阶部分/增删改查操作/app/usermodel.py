# @Time    : 2025/12/22 10:19
# @Author  : hero
# @File    : usermodel.py
from json import JSONEncoder, JSONDecoder

from tortoise.fields import CharField, DatetimeField, BooleanField, IntField, DecimalField, JSONField
from tortoise.models import Model

def validate_age(value):
    if value < 0:
        raise ValueError('Age must be greater than or equal to 0')
class  Student(Model):
    id = IntField(pk=True)
    name = CharField(max_length=50)
    email = CharField(max_length=100,unique=True,null=True,description='学生邮箱,唯一')
    age = IntField(validators=[validate_age])
    class Meta:
        table='students'
        unique_together=(('name','email'))

    def __str__(self):
        return self.name

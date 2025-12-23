# @Time    : 2025/12/22 09:30
# @Author  : hero
# @File    : usermodel.py

from tortoise.models import Model
from tortoise.fields import CharField,DatetimeField,BooleanField,IntField

class  User(Model):
    id = CharField(max_length=30,primary_key=True) #tips:uuid主键
    username = CharField(max_length=20,unique=True)
    email = CharField(max_length=255,unique=True)
    is_active = BooleanField(default=True)
    created_at = DatetimeField(auto_now_add=True) #创建时间
    updated_at = DatetimeField(auto_now=True)
    class Meta:
        table='user'
    def __str__(self):
        return self.username

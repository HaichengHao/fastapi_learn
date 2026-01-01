# @Time    : 2026/1/1 22:21
# @Author  : hero
# @File    : models.py

from tortoise.models import Model
from tortoise import fields
#tips:数据表设置
class UserTB(Model):
    id=fields.IntField(pk=True)
    username=fields.CharField(max_length=32)
    email=fields.CharField(max_length=64,unique=True)
    age=fields.IntField(default=0)
    created_at=fields.DatetimeField(auto_now_add=True)

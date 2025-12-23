# @Time    : 2025/12/22 10:19
# @Author  : hero
# @File    : usermodel.py
from json import JSONEncoder, JSONDecoder

from tortoise.fields import CharField, DatetimeField, BooleanField, IntField, DecimalField, JSONField
from tortoise.models import Model
from tortoise.validators import Validator

#tips:字段验证器
def validate_age(value):
    if value < 0:
        raise ValueError('Age must be greater than or equal to 0')

#tips:模型定义
class User(Model):
    id = IntField(primary_key=True)  # tips:uuid主键 其中主键可以写为pk=True
    username = CharField(max_length=20, unique=True)
    address = CharField(max_length=30, null=True)  # tips:null=True   代表可以为空
    email = CharField(max_length=255, unique=True,index=True)
    age = IntField(validators=[validate_age])  # tips:使用我们自己定义的验证, important  注意，列表中可以传入多个验证规则
    is_active = BooleanField(default=True)
    salary = DecimalField(gt=0, max_digits=10, decimal_places=2)  # tips:最大10位数,包含两位小数 gt=0表示要大于0
    created_at = DatetimeField(auto_now_add=True)  # 创建时间 tips  仅首次保存1记录时间
    updated_at = DatetimeField(auto_now=True)  # tips:auto_now 保存时更新

    # secrets_key=JSONField(null=True,encoder=JSONEncoder,decoder=JSONDecoder)  tips:存储字典或列表,可以自定义编码器和解码器

    #tips:模型元数据
    class Meta:
        table = 'employee'  # tips:自定义表的名称
        ordering = ['-created_at']  # tips:默认创建时间倒序排序
        indexes = [('email')] #tips:为邮件字段创建索引,也可以直接在模型定义中直接写参数index=True
        unique_together = (('username', 'email'),)  #tips:定义联合唯一约束,一个用户只能绑定一个邮箱地址

    def __str__(self):
        return self.username

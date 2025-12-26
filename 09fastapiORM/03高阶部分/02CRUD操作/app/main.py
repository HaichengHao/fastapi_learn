# @Time    : 2025/12/26 12:32
# @Author  : hero
# @File    : main.py
from typing import Annotated

from fastapi import FastAPI, Form

from models import *
from settings import Tortoise_orm
from tortoise.contrib.fastapi import register_tortoise
from pydantic import BaseModel, Field

app = FastAPI()

# register_tortoise(
#     app,
#     config=Tortoise_orm,
#     generate_schemas=False, #tips:因为此次为复用表而非创建新的表，所以这里写为False
#     add_exception_handlers=True
# )

# tips:或者直接写，不用settings里的配置字典
register_tortoise(
    app,
    db_url='mysql://niko:HHCzio20@localhost:3306/fastapidb1',
    modules={'models': ['models']},
    generate_schemas=False
)


class Studentinfo(BaseModel):
    name: str
    age: int
    address: str
    phone: Annotated[str,Field(pattern=r'^1[3-9]\d{9}$')]
    address: str


@app.post('/stu', description='添加学生')
async def addstu(stu: Annotated[Studentinfo, Form()]):
    stu_new = await Student.create(
        name=stu.name,
        age=stu.age
    )
    # tips:因为和档案有一对一关系，所以需要连同档案的也要创建
    profile = await StudentProfile.create(
        address=stu.address,
        phonenum=stu.phone,
    )
    # tips:然后指定学生信息的档案信息
    stu_new.profile = profile  # important:注意这里相当于修改数据
    # important：所以需要save,如果只是创建而不是我们这样后面又进行类似修改操作的参数指定的话就不需要save
    await stu_new.save()

    #tips:当然了，也可以换个顺序，这样就不需要上面那么繁琐
    #
    #
    # profile = await StudentProfile.create(
    #     address=stu.address,
    #     phonenum=stu.phone,
    # )
    # stu_new = await Student.create(
    #     name=stu.name,
    #     age=stu.age
    # )
    # stu_new.profile = profile

    return {
        'status': True,
        'msg': f'学生-{stu_new.name}信息录入成功'
    }

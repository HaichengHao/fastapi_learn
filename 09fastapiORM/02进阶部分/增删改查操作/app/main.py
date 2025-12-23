# @Time    : 2025/12/22 10:18
# @Author  : hero
# @File    : main.py
from unicodedata import name

from fastapi import FastAPI, Form
from pydantic import BaseModel
from typing import Annotated, Optional
from aerichconfig import Tortoise_orm
from usermodel import Student
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()

register_tortoise(
    app,
    config=Tortoise_orm,
    generate_schemas=True,
    add_exception_handlers=True
)


# tips:接口方式
class Stu(BaseModel):
    name: str
    age: int
    email: str


# tips:restful写法，一个路由干多个事
@app.post('/stu')
async def adduser(stu: Annotated[Stu, Form()]):
    await Student.create(name=stu.name, age=stu.age, email=stu.email)
    return {
        'status': True,
        'message': f'Student{stu.name} successfully added'
    }


@app.delete('/stu', description='传入学生id对其进行删除')
async def get_stu(id: int):
    stu = await Student.get(id=id)
    if stu:
        await stu.delete()
        return {
            'status': True,
            'message': f'Student{stu.name} successfully retrieved'
        }


# class updateForm(BaseModel):
#     id: int = Form()
#     name: str | None = None
#     age: int | None = None
#     email: str | None = None
#


# @app.patch('/stu', description='修改学生信息')
# async def update_stu(stu: Annotated[updateForm, Form()]):
#     targetstu = await Student.get(id=stu.id)
#     if not targetstu:
#         return {
#             'msg': '未查到该🧑‍🎓学生信息,请检查id'
#         }
#     else:
#         if stu.name:
#             targetstu.name = stu.name
#         if stu.age:
#             targetstu.age = stu.age
#         if stu.email:
#             targetstu.email = stu.email
#
#     await targetstu.save()
#     return {
#         'status': True,
#         'message': f'Student{targetstu.name} successfully updated'
#     }


class UpdateStudentForm(BaseModel):
    id: int
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None


@app.patch('/stu', description='修改学生信息（传入 id 和要修改的字段）')
async def update_stu(form: UpdateStudentForm):
    student = await Student.get_or_none(id=form.id)
    if not student:
        return {"status": False, "msg": "学生不存在"}

    # tips： 只更新客户端实际提供的字段（排除 id 和 None 值）
    update_fields = form.model_dump(exclude_unset=True)
    update_fields.pop("id", None)

    if not update_fields:
        return {"status": True, "msg": "无字段需要更新"}

    await Student.filter(id=form.id).update(**update_fields)  # tips:进行批量更新

    updated = await Student.get(id=form.id)
    return {"status": True, "message": f"学生 {updated.name} 更新成功", "data": updated}


@app.get('/stu/{id}', response_model=Stu, description='根据ID查询单个学生')
async def get_student_by_id(id: int):
    stu = await Student.get(id=id)
    return stu


@app.get('/stus', description='查询学生信息', response_model=list[Stu])
async def get_stu(name:str):  # tips:一个查询参数id,如果输入就查询单个学生，否则查询多个
    allstu = await Student.filter(name__contains=name)
    return allstu


@app.get('/stu',description='模糊查询',response_model=list[Stu])
async def get_stu():
    stu = await Student.get()
    return stu
# @Time    : 2025/12/26 12:32
# @Author  : hero
# @File    : main.py
from typing import Annotated
from fastapi_pagination import add_pagination, Page, Params
from fastapi_pagination.ext.tortoise import apaginate
from fastapi import FastAPI, Form, HTTPException
from typing import Optional
from models import *
from settings import Tortoise_orm
from tortoise.contrib.fastapi import register_tortoise
from pydantic import BaseModel, Field

app = FastAPI()
add_pagination(app)

# register_tortoise(
#     app,
#     config=Tortoise_orm,
#     generate_schemas=False, #tips:因为此次为复用表而非创建新的表，所以这里写为False
#     add_exception_handlers=True #tips:生产环境不要开这个
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
    phone: Annotated[str, Field(pattern=r'^1[3-9]\d{9}$')]


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

    # tips:当然了，也可以换个顺序，这样就不需要上面那么繁琐
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


# tips:查询所有学生的基本信息
class BaseStuinfo(BaseModel):
    stuid: int
    name: str
    age: int


@app.get('/stuall', response_model=Page[BaseStuinfo])
async def get() -> Page[BaseStuinfo]:
    return await apaginate(Student)


# tips:查询所有学生的基本信息之前后端不分离模式
from fastapi import Request
from fastapi.templating import Jinja2Templates


@app.get('/stuallinfo', response_model=Page[BaseStuinfo])
async def get(request: Request) -> Page[BaseStuinfo]:
    templates = Jinja2Templates(directory='../templates')
    allstu = await apaginate(Student)
    return templates.TemplateResponse('index.html', {
        'request': request,
        'all_stu': allstu
    })


# tips:查询详细信息

@app.get('/stu/{stuid}', description='查询详细学生信息', response_model=Studentinfo)
async def get_stu(stuid: int):
    target_stu = await Student.get(stuid=stuid).prefetch_related('profile')
    if not target_stu.profile:
        raise HTTPException(status_code=404, detail='学生档案未找到')
    return Studentinfo(
        name=target_stu.name,
        age=target_stu.age,
        address=target_stu.profile.address,
        phone=target_stu.profile.phonenum
    )


# tips:修改学生信息
class UpdateStu(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    address: Optional[str] = None


@app.patch('/stu/{stuid}', description='修改学生信息')
async def update_student(stuid: int, form: UpdateStu):  # ← 用 UpdateStu 模型！
    # 获取学生及其档案
    student = await Student.get_or_none(stuid=stuid).prefetch_related('profile')
    if not student:
        raise HTTPException(status_code=404, detail='学生未找到')

    # 更新 Student 表字段（name, age）
    update_data = form.model_dump(exclude_unset=True) #tips:这样出来是一个字典
    student_update = {}


    if 'name' in update_data:
        student_update['name'] = update_data['name']
    if 'age' in update_data:
        student_update['age'] = update_data['age']

    if student_update:
        await Student.filter(stuid=stuid).update(**student_update)

    # 更新 StudentProfile 表字段（address）
    if 'address' in update_data and student.profile:
        await student.profile.update_from_dict({'address': update_data['address']}).save()

    if 'phone' in update_data and student.profile:
        await student.profile.update_from_dict({'phonenum': update_data['phone']}).save()
    return {
        'status': True,
        'msg': f'学生 {stuid} 信息更新成功'
    }


# tips:删除学生
@app.delete('/stu/{stuid}', description='删除学生')
async def delstu(stuid: int):
    targetstu = await Student.get(stuid=stuid).prefetch_related('profile')
    if not targetstu.profile:
        raise HTTPException(detail='学生未找到')
    else:
        await targetstu.delete()
        return {
            'status': True,
            'msg': f'删除{targetstu.name}信息成功!!'
        }

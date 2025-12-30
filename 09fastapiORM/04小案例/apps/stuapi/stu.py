# @Time    : 2025/12/29 09:43
# @Author  : hero
# @File    : stu.py

from fastapi import APIRouter, Form
from pydantic import BaseModel
from models.stumodel import *
from typing import Optional, Annotated

stu_router = APIRouter()


class Stu(BaseModel):
    name: str
    age: int
    pwd: str
    sno: int
    clasid: int


@stu_router.get("/", response_model=Stu)
async def get_stu():
    pass


@stu_router.get("/stu/{id}", response_model=Stu)
async def get_stu_by_id(id: int):
    targetstu = await Student.get(id=id)
    return {
        'code': 200,
        'stuinfo': targetstu
    }


@stu_router.delete("/stu/{id}")
async def delete_stu_by_id(id: int):
    pass


@stu_router.post("/")
async def create_stu(stu: Annotated[Stu, Form()]):
    cls =await  Clas.create(
        id=stu.clasid
    )
    stu=await Student.create(
        name=stu.name,
        age=stu.age,
        pwd=stu.pwd,
        sno=stu.sno,
    )
    stu.clas=cls

    return {
        'code': 201,
        'msg': f'{stu.name}信息录入成功'
    }


@stu_router.put("/{id}")
async def update_stu(id: int, stu: Stu):
    pass

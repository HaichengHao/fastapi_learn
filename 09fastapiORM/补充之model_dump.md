## .model_dump()

> 有时候我们创建表的时候可能会这样写

```python
class UserTB(Model):
    id=fields.IntField(pk=True)
    username=fields.CharField(max_length=32)
    email=fields.CharField(max_length=64,unique=True)
    age=fields.IntField(default=0)
    created_at=fields.DatetimeField(auto_now_add=True)


#tips:schema定义,输入输出校验
class  Users(BaseModel):
    username:str
    email:str
    age:int


#tips:路由定义

@user_router.post('/create')
async def create_user(user:Users):
    await UserTB.create(
        username=user.username,
        email=user.email,
        age=user.age
    )

```

> 但是我们每次都单独指定字段名和值是有些费时间的，尤其是表字段庞大的时候
> 这时候可采用model_dump

```python
@user_router.post('/create')
async def create_user(user:Users):
    # await UserTB.create(
        # username=user.username,
        # email=user.email,
        # age=user.age  
    #tips:我们可以用一个简单的方式,和上面的效果是一样的,
    #important：⚠️但是这个有要求，就是schema字段的名称要和数据表字段的名称一致
    user_new=await UserTB.create(
        **user.model_dump()
    )
    return user_new

 
```
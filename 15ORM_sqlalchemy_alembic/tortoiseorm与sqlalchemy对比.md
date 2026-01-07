当然可以！下面是一个清晰、实用的对比表，展示 **SQLAlchemy（配合 SQLModel 或原生 ORM）** 与 **Tortoise-ORM** 在 **FastAPI 路由中实现 CRUD 操作** 的主要差异，涵盖语法、异步支持、依赖注入、模型定义等方面。

---

## 🆚 SQLAlchemy vs Tortoise-ORM：FastAPI 中 CRUD 对比表

| 特性 | **SQLAlchemy（+ SQLModel / async SQLAlchemy）** | **Tortoise-ORM** |
|------|-----------------------------------------------|------------------|
| **ORM 类型** | 通用 ORM（支持同步/异步） | **专为 asyncio 设计** 的异步 ORM |
| **FastAPI 官方推荐** | ✅（通过 `sqlmodel` 作者 same as FastAPI 作者） | ❌（社区流行，但非官方） |
| **模型定义** | 使用 `SQLModel` 或 `DeclarativeBase` + `Mapped` | 继承 `tortoise.models.Model` |
| **数据库连接** | 需手动创建 `AsyncEngine` + `AsyncSession` | 通过 `Tortoise.init()` 全局初始化 |
| **依赖注入** | 需自定义 `get_session()` 依赖 | 通常直接在路由中使用模型方法（无 session 概念） |
| **查询语法** | 基于 `select()` + `session.execute()` | 链式调用 `.filter().get()` 等 |
| **迁移工具** | ✅ Alembic（强大、成熟） | ❌ 无官方迁移工具（需 `aerich` 第三方） |
| **类型提示支持** | ✅ 极佳（尤其 SQLModel） | ⚠️ 较弱（部分操作返回 `Any`） |
| **学习曲线** | 中等（需理解 session、engine） | 简单（Django 风格） |

---

### 🔍 CRUD 操作代码对比（以 `Employee` 模型为例）

#### 1. **模型定义**

| SQLAlchemy (SQLModel) | Tortoise-ORM |
|------------------------|--------------|
```python
# models.py
from sqlmodel import SQLModel, Field
from datetime import datetime

class Employee(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=50)
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
```
```python
# models.py
from tortoise.models import Model
from tortoise import fields
from datetime import datetime

class Employee(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
```

---

#### 2. **创建（Create）**

| SQLAlchemy | Tortoise-ORM |
|-----------|--------------|
```python
@app.post("/employees/", response_model=Employee)
async def create(emp: Employee, session: AsyncSession = Depends(get_session)):
    session.add(emp)
    await session.commit()
    await session.refresh(emp)
    return emp
```
```python
@app.post("/employees/", response_model=Employee_Pydantic)
async def create(emp: EmployeeIn_Pydantic):
    obj = await Employee.create(**emp.model_dump())
    return await Employee_Pydantic.from_tortoise_orm(obj)
```

> 💡 Tortoise 需要 Pydantic 模型做序列化（如 `Employee_Pydantic`）

---

#### 3. **读取（Read）**

| SQLAlchemy | Tortoise-ORM |
|-----------|--------------|
```python
@app.get("/employees/{id}", response_model=Employee)
async def read(id: int, session: AsyncSession = Depends(get_session)):
    emp = await session.get(Employee, id)
    if not emp: raise HTTPException(404)
    return emp
```
```python
@app.get("/employees/{id}", response_model=Employee_Pydantic)
async def read(id: int):
    emp = await Employee.get_or_none(id=id)
    if not emp: raise HTTPException(404)
    return await Employee_Pydantic.from_tortoise_orm(emp)
```

---

#### 4. **更新（Update）**

| SQLAlchemy | Tortoise-ORM |
|-----------|--------------|
```python
@app.put("/employees/{id}")
async def update(id: int, data: EmployeeUpdate, session: AsyncSession = Depends(get_session)):
    emp = await session.get(Employee, id)
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(emp, key, val)
    await session.commit()
    return emp
```
```python
@app.put("/employees/{id}")
async def update(id: int, data: EmployeeIn_Pydantic):
    await Employee.filter(id=id).update(**data.model_dump())
    emp = await Employee.get(id=id)
    return await Employee_Pydantic.from_tortoise_orm(emp)
```

---

#### 5. **删除（Delete）**

| SQLAlchemy | Tortoise-ORM |
|-----------|--------------|
```python
@app.delete("/employees/{id}")
async def delete(id: int, session: AsyncSession = Depends(get_session)):
    emp = await session.get(Employee, id)
    await session.delete(emp)
    await session.commit()
    return {"deleted": True}
```
```python
@app.delete("/employees/{id}")
async def delete(id: int):
    deleted_count = await Employee.filter(id=id).delete()
    if not deleted_count: raise HTTPException(404)
    return {"deleted": True}
```

---

### 🛠 项目初始化对比

| 任务 | SQLAlchemy | Tortoise-ORM |
|------|-----------|--------------|
| **数据库连接** | `create_async_engine` + `AsyncSession` | `Tortoise.init(db_url=..., modules=["models"])` |
| **启动时初始化** | 可选（Alembic 建表） | 必须调用 `Tortoise.init()` |
| **关闭连接** | 通常不需要（FastAPI 生命周期管理） | 需在 shutdown 事件中 `await Tortoise.close_connections()` |
| **迁移** | `alembic revision --autogenerate` | `aerich init -t config.TORTOISE_ORM` → `aerich migrate` |

---

### ✅ 何时选择哪个？

| 场景 | 推荐 |
|------|------|
| 需要强大迁移（生产级） | ✅ **SQLAlchemy + Alembic** |
| 快速原型 / 小项目 / 喜欢 Django 风格 | ✅ **Tortoise-ORM** |
| 强类型提示 + Pydantic 集成 | ✅ **SQLModel（SQLAlchemy 上层）** |
| 复杂查询（JOIN、子查询） | ✅ **SQLAlchemy（表达力更强）** |
| 不想写 session 管理 | ✅ **Tortoise-ORM** |

---

### 📌 总结口诀

> - **SQLAlchemy：灵活强大，适合长期维护**  
> - **Tortoise：简单快捷，适合快速开发**  
> - **两者都支持异步，但设计理念不同**  
> - **FastAPI 官方示例多用 SQLModel（即 SQLAlchemy）**

---

如果你正在构建一个 **需要长期演进、有复杂业务逻辑、重视数据迁移** 的系统，**SQLAlchemy + Alembic 是更稳健的选择**。  
如果你只是做一个 **小型 API 或 MVP**，**Tortoise-ORM 会更快上手**。

需要我为你生成一个完整的 Tortoise-ORM + FastAPI 示例吗？欢迎继续提问！😊
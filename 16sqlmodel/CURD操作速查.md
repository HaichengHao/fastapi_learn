当然可以！下面我将手把手教你用 **SQLModel + FastAPI** 实现一套**完整、类型安全、可直接用于生产**的简单 CRUD（Create, Read, Update, Delete）接口。

我们将以 `Hero`（英雄）模型为例，包含字段：`id`, `name`, `secret_name`, `age`。

---

## 🧰 技术栈

- **FastAPI**：Web 框架
- **SQLModel**：数据库模型（基于 SQLAlchemy 2.0）
- **SQLite**：本地开发数据库（无需安装 PostgreSQL）
- **Pydantic**：自动请求/响应验证（已内置在 SQLModel 中）

---

## 📁 项目结构（极简版）

```
sqlmodel-crud/
├── main.py
└── requirements.txt
```

---

## 第一步：安装依赖 (`requirements.txt`)

```txt
fastapi[all]
uvicorn[standard]
sqlmodel
```

安装：
```bash
pip install -r requirements.txt
```

---

## 第二步：编写代码 (`main.py`)

```python
# main.py
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import List, Optional
import os

# ======================
# 1. 定义数据模型
# ======================
class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)          # 可索引，加速查询
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)


# ======================
# 2. 数据库设置
# ======================
# 使用 SQLite 文件数据库（开发友好）
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./heroes.db")
# 注意：SQLModel 在 SQLite 下默认不支持并发写入，仅用于开发！

engine = create_engine(DATABASE_URL, echo=True)  # echo=True 打印 SQL 日志

# 创建表（如果不存在）
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# 依赖项：获取数据库会话
def get_session():
    with Session(engine) as session:
        yield session


# ======================
# 3. FastAPI 应用
# ======================
app = FastAPI(title="SQLModel CRUD 示例")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# ======================
# 4. CRUD 接口
# ======================

# ✅ Create
@app.post("/heroes/", response_model=Hero)
def create_hero(hero: Hero, session: Session = Depends(get_session)):
    session.add(hero)
    session.commit()
    session.refresh(hero)  # 获取数据库生成的 id
    return hero


# ✅ Read (List)
@app.get("/heroes/", response_model=List[Hero])
def read_heroes(offset: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


# ✅ Read (Single)
@app.get("/heroes/{hero_id}", response_model=Hero)
def read_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


# ✅ Update
@app.patch("/heroes/{hero_id}", response_model=Hero)
def update_hero(hero_id: int, hero_update: Hero, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    
    # 更新字段（只更新非 None 值）
    hero_data = hero_update.dict(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(hero, key, value)
    
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


# ✅ Delete
@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}
```

---

## ▶️ 第三步：运行应用

```bash
uvicorn main:app --reload
```

访问：http://localhost:8000/docs  
你会看到 **自动生成的 Swagger UI**，可以直接测试所有接口！

---

## 🧪 测试 CRUD 操作（通过 Swagger 或 curl）

### 1. 创建英雄（POST `/heroes/`）
```json
{
  "name": "Spider-Boy",
  "secret_name": "Peter Parker",
  "age": 18
}
```
→ 返回带 `id` 的完整对象

### 2. 获取所有英雄（GET `/heroes/`）
→ 返回列表，支持分页（`?offset=0&limit=5`）

### 3. 获取单个英雄（GET `/heroes/1`）
→ 返回 id=1 的英雄

### 4. 更新英雄（PATCH `/heroes/1`）
```json
{
  "age": 19
}
```
→ 只更新 `age`，其他字段不变

### 5. 删除英雄（DELETE `/heroes/1`）
→ 返回 `{"ok": true}`

---

## 🔍 关键知识点解析

### ✅ 为什么 `id` 是 `Optional[int]`？
- 因为插入时数据库自动生成 `id`，你不需要提供
- 但读取时它一定存在 → SQLModel + Pydantic 能正确处理这种“输入可选，输出必有”的场景

### ✅ `response_model=Hero` 的作用
- 自动过滤掉你不希望返回的字段（比如密码）
- 本例中所有字段都公开，所以直接用 `Hero`

### ✅ `hero_update: Hero` 用于 PATCH
- 利用 Pydantic 的 `.dict(exclude_unset=True)` 只获取用户实际发送的字段
- 避免把未提供的字段设为 `None`

### ✅ `select(Hero)` 是 SQLAlchemy 2.0 风格
- 替代了旧版的 `session.query(Hero)`
- 更灵活，支持复杂查询（如 join、filter）

---

## 🛠 进阶建议（生产准备）

| 功能 | 如何加 |
|------|--------|
| **请求验证** | SQLModel 自动继承 Pydantic，字段类型/必填已校验 |
| **分页响应** | 自定义 Pydantic 模型：`Page[Hero]` |
| **搜索/过滤** | 在 `read_heroes` 中加 `name: str = None`，用 `select.where(Hero.name == name)` |
| **换 PostgreSQL** | 改 `DATABASE_URL = "postgresql://user:pass@localhost/db"` |
| **异步支持** | 用 `sqlalchemy.ext.asyncio` + `AsyncSession`（需改写）|

> 💡 当前示例使用**同步 Session**，适合中小型应用。若需高并发，可升级到异步（稍复杂）。

---

## ✅ 总结

你现在已经掌握了：

- ✅ 用 SQLModel 定义模型
- ✅ 用 FastAPI 写标准 CRUD
- ✅ 自动获得 OpenAPI 文档
- ✅ 类型安全 + 请求验证

这套代码**可以直接用于真实项目原型或中小型应用**！

---

如果你想要：
- ✅ **异步版本（AsyncSession）**
- ✅ **带搜索和分页的增强版**
- ✅ **关联模型（一对多）CRUD 示例**

告诉我，我可以继续为你扩展！现在就可以运行试试看 😊
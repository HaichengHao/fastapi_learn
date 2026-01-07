当然可以！以下是一份 **SQLModel + Alembic 速查表（Cheat Sheet）**，专为 FastAPI 开发者设计，涵盖从环境搭建、模型定义、数据库连接、CRUD 操作到迁移管理的完整流程。内容结构清晰、代码可直接运行，适合学习与日常参考。

---

# 📘 SQLModel + Alembic 速查表（FastAPI 专用）

> ✅ 基于 **SQLModel v0.0.22+** + **Alembic v1.13+** + **PostgreSQL / SQLite**  
> ✅ 支持 **异步（Async）** 和 **同步（Sync）**（本表以 **异步为主**）

---

## 一、安装依赖

```bash
pip install fastapi "sqlmodel[asyncpg]" alembic uvicorn
# 若用 SQLite 替换 asyncpg → aiosqlite
# pip install "sqlmodel[aiosqlite]"
```

---

## 二、项目结构建议

```
myapp/
├── main.py               # FastAPI 入口
├── models/               # 数据库模型
│   └── user.py
├── database.py           # DB 连接 & Session
├── alembic.ini           # Alembic 配置（自动生成）
└── alembic/              # 迁移脚本目录（自动生成）
    ├── env.py
    └── versions/
```

---

## 三、数据库连接（`database.py`）

```python
# database.py
from sqlmodel import create_engine, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import os

# 使用 PostgreSQL（推荐生产）
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://nikofox:HHCzio20.@localhost/mydb")

# 使用 SQLite（开发测试）
# DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async def init_db():
    async with engine.begin() as conn:
        # 注意：SQLModel.metadata.create_all 不适用于异步！
        await conn.run_sync(SQLModel.metadata.create_all)

# Session 工厂
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
```

> 💡 **重要**：异步模式下不能直接调 `SQLModel.metadata.create_all(engine)`，必须用 `conn.run_sync()`。

---

## 四、定义模型（`models/user.py`）

```python
# models/user.py
from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    email: str = Field(unique=True, max_length=255)
    is_active: bool = Field(default=True)

    # 可选：配置表名
    # class Config:
    #     table_name = "users"
```

> ✅ 自动同时作为：
> - SQLAlchemy 表模型（用于 DB）
> - Pydantic 模型（用于 API 请求/响应）

---

## 五、FastAPI 路由示例（`main.py`）

```python
# main.py
from fastapi import FastAPI, Depends
from models.user import User
from database import get_session, init_db
from sqlmodel.ext.asyncio.session import AsyncSession

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.post("/users/", response_model=User)
async def create_user(user: User, session: AsyncSession = Depends(get_session)):
    session.add(user)
    await session.commit()
    await session.refresh(user)  # 获取自增 ID
    return user

@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    return user
```

---

## 六、Alembic 初始化与配置

### 1. 初始化 Alembic

```bash
alembic init alembic
```

### 2. 修改 `alembic.ini`

```ini
# alembic.ini
sqlalchemy.url = postgresql+asyncpg://nikofox:HHCzio20.@localhost/mydb
# 或 SQLite: sqlite+aiosqlite:///./test.db
```

### 3. 修改 `alembic/env.py`（关键！支持 SQLModel）

```python
# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import SQLModel
from alembic import context
import asyncio
from database import DATABASE_URL  # 引入你的 DB URL

# 导入所有模型（确保 metadata 包含所有表）
from models.user import User  # 👈 必须导入！

config = context.config
config.set_main_option('sqlalchemy.url', DATABASE_URL)

if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations():
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online():
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

> ⚠️ **必须导入所有模型**（如 `from models.user import User`），否则 Alembic 找不到表！

---

## 七、常用 Alembic 命令

| 操作 | 命令 |
|------|------|
| 生成新迁移 | `alembic revision --autogenerate -m "add user table"` |
| 应用迁移 | `alembic upgrade head` |
| 回滚一次 | `alembic downgrade -1` |
| 查看历史 | `alembic history` |
| 查看当前版本 | `alembic current` |
| 创建空迁移（手动写） | `alembic revision -m "custom sql"` |

> ✅ `--autogenerate` 能自动检测：
> - 新增/删除表
> - 新增/删除列
> - 修改列类型（部分支持）
> - 添加索引/唯一约束

---

## 八、常见 CRUD 操作（异步）

```python
# 创建
user = User(name="Alice", email="a@example.com")
session.add(user)
await session.commit()
await session.refresh(user)  # 获取 ID

# 查询单条
user = await session.get(User, 1)

# 查询多条（使用 select）
from sqlmodel import select
statement = select(User).where(User.is_active == True)
users = (await session.exec(statement)).all()

# 更新
user.name = "New Name"
session.add(user)
await session.commit()

# 删除
await session.delete(user)
await session.commit()
```

---

## 九、高级技巧

### 1. 分离“创建模型”与“数据库模型”

```python
class UserBase(SQLModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
```

> 用于避免前端传入 `id` 等只读字段。

### 2. 自定义主键/索引

```python
from sqlmodel import Field, Index

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(sa_column=Column("email", String, unique=True, index=True))
```

或使用 `__table_args__`：

```python
class User(SQLModel, table=True):
    __table_args__ = (Index("idx_email", "email"),)
    ...
```

---

## 十、调试与最佳实践

- ✅ **始终在 `env.py` 中导入所有模型**
- ✅ 开发时开启 `echo=True` 查看 SQL
- ✅ 使用 `.env` 管理数据库 URL
- ❌ 不要在异步函数中调用同步的 `create_all()`
- ✅ 迁移前先备份数据库（生产环境！）
- ✅ 使用 `response_model=UserRead` 避免返回密码等敏感字段

---

## 📚 推荐学习资源

- 官方文档：https://sqlmodel.tiangolo.com/
- Alembic 文档：https://alembic.sqlalchemy.org/
- GitHub 示例模板：`fastapi-sqlmodel-async-template`

---

你可以将此速查表保存为 `sqlmodel-alembic-cheatsheet.md`，配合实际项目边学边用。如果需要我提供一个**完整可运行的 GitHub 项目模板**（含 Docker、pytest、用户注册登录等），也可以告诉我！祝你学习顺利！🚀
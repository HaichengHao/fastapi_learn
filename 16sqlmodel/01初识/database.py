# @Time    : 2026/1/6 13:03
# @Author  : hero
# @File    : database.py

from sqlmodel import create_engine, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import QueuePool

engine = create_async_engine(
    url=os.getenv('DATABASE_URL'),
    echo=True,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={ #important：数据库链接参数
        'timeout': 30,
        'command_timeout': 30,
    }

)

# tips:session工厂
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

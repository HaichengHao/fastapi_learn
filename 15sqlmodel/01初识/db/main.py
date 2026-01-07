# @Time    : 2026/1/6 16:03
# @Author  : hero
# @File    : main.py
from dns.entropy import pool
#important:创建异步引擎

from sqlalchemy.ext.asyncio import AsyncEngine,create_async_engine,async_sessionmaker


from ..config import project_configs
from sqlalchemy.pool import QueuePool
engine=create_async_engine(
    url=project_configs.DATABASE_URL,
    echo=True,
    pool_class=QueuePool,
    pool_size=20,
    max_overflow=10,
    pool_recycle=3600,
    connect_args={
        'timeout': 30,
        'command_timeout': 30,
    }
)
AsyncSessionLocal=async_sessionmaker(
    engine,expire_on_commit=False
)
"""
@File    :cr_asyncengine.py
@Editor  : 百年
@Date    :2026/2/9 19:27 
"""

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker
from config import Config
from src.models.employee import Employee  #important:显式导入
from src.models import Base
__all__=['Employee']
#tips:创建异步引擎
engine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True
)

#important:创建一个异步函数用于声明周期事件

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session() -> AsyncSession:
    AsyncSessionlocal = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession
    )
    async with AsyncSessionlocal() as session:
        yield session


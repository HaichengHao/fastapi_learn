# @Time    : 2026/1/6 16:52
# @Author  : hero
# @File    : database.py

from sqlalchemy import create_engine

#tips:创建引擎
engine = create_engine('postgresql+asyncpg://nikofox:HHCzio20.@localhost:5432/nikofox')


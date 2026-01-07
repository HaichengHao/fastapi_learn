# @Time    : 2026/1/6 17:30
# @Author  : hero
# @File    : db_main.py
from pydoc import cram

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.engine import create_engine

engine = create_engine( #tips:这里我们先用同步阻塞
    url='mysql+pymysql://niko:HHCzio20@localhost:3306/fastapidb4',
    echo=False
)


#tips:定义一个模型的基类,如果想加一些数据表都有的东西就得这么写
# class  Base(DeclarativeBase):
#     pass
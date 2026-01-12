# @Time    : 2026/1/12 13:37
# @Author  : hero
# @File    : __init__.py.py


from sqlalchemy.orm import DeclarativeBase,sessionmaker,create_session,Mapped,MappedColumn
from sqlalchemy import create_engine


engine = create_engine(
    url='mysql+pymysql://niko:HHCzio20@localhost:3306/fastapidb4',
    echo=False,
    pool_size=20,
    max_overflow=10,
    pool_per_ping=True,
    connect_args={
        'timeout':60,
        'command_timeout':60,
    }

)

class Base(DeclarativeBase):
    pass
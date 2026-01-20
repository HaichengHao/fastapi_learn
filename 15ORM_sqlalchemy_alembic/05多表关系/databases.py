# @Time    : 2026/1/20 17:27
# @Author  : hero
# @File    : databases.py

from models.employee import Employee
from models.department import Department
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, Session
from models.employee import Employee, GenderValue,IDCard
engin  = create_engine(
    url='mysql+pymysql://niko:HHCzio20@localhost:3306/fastapidb4',
    echo=False
)

def get_session():
    session = Session(bind=engin)
    try:
        yield session #important:返回生成对象session并在此暂停,等下次继续拿session对象进行数据库会话操作的时候就在此处继续,非常高效
    finally:
        session.close()
# @Time    : 2026/1/6 15:59
# @Author  : hero
# @File    : tstconfig.py

from config import Settings
s=Settings() #tips:实例化类对象
print(s.DATABASE_URL)
'''
/home/nikofox/fastapi_learn/.venvs/bin/python /home/nikofox/fastapi_learn/15sqlmodel/01初识/tstconfig.py 
postgresql+asyncpg://nikofox:HHCzio20.@localhost:5432/nikofox

Process finished with exit code 0
正确拿到了!!'''
# @Time    : 2025/12/21 23:37
# @Author  : hero
# @File    : 01初体验.py

'''
需要pip install
tortoise-orm 一个对象关系模型
aerich  将我们的类，属性这样的翻译成sql
aiomysql 专门将aerich这样翻译出的sql交给mysql来处理sql语句,它是异步的，我们可以理解它会帮我们生成配置文件
tomlkit 帮我们管理配置文件的
'''

# tips:tortoise-rom需要一个配置字典来定义数据库连接信息，通常存储在settings.py或类似的配置文件中
# 就像flask那样
from fastapi import FastAPI
from typing import Annotated, Dict
from tortoise.contrib.fastapi import register_tortoise

# tips:数据库配置 非常像django中的写法
Torroise_orm: Dict = {
    'connections': {
        # 开发环境可以使用sqlite(基于文件，无需服务器)
        # 'default':'sqlite://db.sqlite3',
        # 生产环境会用到psql,mysql等
        # 'default':'postgres://user:password@locahost:5432/dbname',

        # 'default':'mysql://user:password@locahost:3306/dbname'
        'default': 'mysql://niko:HHCzio20@locahost:3306/fastapidb'

    },
    'apps': {
        'models': {
            # 'models': ['app.models', 'aerich.models'],  # tips 模型板块和Aerich迁移模型
            'models': ['aerich.models'],  # tips 模型板块和Aerich迁移模型
            'default_connection': 'default',  # tips:指定使用我们上面定义的默认数据库连接
        }
    },
    # important:连接池配置(推荐)
    'use_tz': False,  # 是否使用时区
    'timezone': 'UTC',  # 默认时区
    'db_pool': {
        'max_size': 10,  # 最大连接数
        'min_size': 1,  # 最小连接数
        'idle_timeout': 30,  # 空闲连接超时(秒)
    }
}

app = FastAPI()

register_tortoise(
    app, config=Torroise_orm,
    generate_schemas=True,
    add_exception_handlers=True)  # tips:调用参数对app进行数据库配置,并指定生成schemas,且添加异常处理器



@app.get('/item')
async def get_item(item):
    return item

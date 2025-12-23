# @Time    : 2025/12/22 09:20
# @Author  : hero
# @File    : config.py
'''
需要pip install
tortoise-orm 一个对象关系模型
aerich  将我们的类，属性这样的翻译成sql
aiomysql 专门将aerich这样翻译出的sql交给mysql来处理sql语句,它是异步的，我们可以理解它会帮我们生成配置文件
tomlkit 帮我们管理配置文件的
'''

'''
Aerich初始化(类似flask的初始化操作)
aerich init -t main.TORTOISE_ORM  main是你主程序的名字，TORTOISE_ORM是你配置的字典，本项目中就是code.Tortoise_orm
这将生成
pyproject.toml:Aerich配置文件，指定迁移配置
migrations/ :迁移文件目录，存放生成的sql文件
aerich init-db

生成和应用迁移(整体上和flask还是很相似的)
生成迁移文件
- 生成迁移文件：当模型发生变更时,运行以下命令生成迁移文件
aerich migarte --name "info"
-应用迁移：运行一下命令将迁移应用到数据库
aerich upgrade
-验证迁移:检查迁移历史
aerich history
- 回滚迁移:回到指定版本
aerich downgrade  

'''


# tips:tortoise-rom需要一个配置字典来定义数据库连接信息，通常存储在settings.py或类似的配置文件中
# 就像flask那样
from fastapi import FastAPI
from typing import Annotated, Dict
from tortoise.contrib.fastapi import register_tortoise

# tips:数据库配置 非常像django中的写法
Tortoise_orm: Dict = {
    'connections': {
        'default': 'mysql://niko:HHCzio20@localhost:3306/fastapidb'

    },
    'apps': {
        'models': {
            # 'models': ['app.models', 'aerich.models'],  # tips 模型板块和Aerich迁移模型
            'models': ['usermodel','aerich.models'],  # tips 模型板块和Aerich迁移模型,这里使用我自己写的usermodel
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
    app, config=Tortoise_orm,
    generate_schemas=True,
    add_exception_handlers=True)  # tips:调用参数对app进行数据库配置,并指定生成schemas,且添加异常处理器

#
#
# @app.get('/item')
# async def get_item(item):
#     return item

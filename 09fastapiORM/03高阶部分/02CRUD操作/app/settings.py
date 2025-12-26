# @Time    : 2025/12/26 12:32
# @Author  : hero
# @File    : settings.py
# @Time    : 2025/12/25 09:51

from fastapi import FastAPI
from typing import Dict

# tips:数据库配置 非常像django中的写法
Tortoise_orm: Dict = {
    'connections': {
        'default': 'mysql://niko:HHCzio20@localhost:3306/fastapidb1'

    },
    'apps': {
        'models': {
            'models': ['models', 'aerich.models'],  # tips 模型板块和Aerich迁移模型,这里使用我自己写的usermodel
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

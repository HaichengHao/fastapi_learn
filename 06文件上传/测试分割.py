# @Time    : 2025/12/18 10:11
# @Author  : hero
# @File    : 测试分割.py
import os

filepath = 'demo.png'
demo = os.path.splitext(filepath)
demosplit = os.path.splitext(filepath)[1]
print(demo)
print(demosplit)
'''('demo', '.png') <--split ext(insion) 就是用来划分文件扩展格式的,它返回的是一个元组，元组中的元素是文件名和'.扩展名'
.png <--它会直接
'''
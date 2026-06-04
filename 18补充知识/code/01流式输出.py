"""
@File    :01流式输出.py
@Editor  : 百年
@Date    :2026/6/4 10:23 
"""
import asyncio

import  uvicorn
# from pyexpat.errors import messages

'''
使用场景
例如，如果你想直接从 AI LLM 服务的输出中流式传输纯文本字符串，就可以使用此功能。

你也可以用它来流式传输大文件，在读取数据的同时逐块发送，而不必一次性将整个文件读入内存。

你还可以通过这种方式流式传输视频或音频，甚至可以在处理和发送数据的同时动态生成它们
'''
from fastapi import FastAPI
from collections.abc import AsyncIterable,Iterable
from fastapi.responses import StreamingResponse

from fastapi.middleware.cors import CORSMiddleware


app=FastAPI(
    prefix='/api/v1',
    description='测试流式输出'
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发时可用，生产环境应限制来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
messages="""
Rick: (stumbles in drunkenly, and turns on the lights) Morty! You gotta come on. You got--... you gotta come with me.
Morty: (rubs his eyes) What, Rick? What's going on?
Rick: I got a surprise for you, Morty.
Morty: It's the middle of the night. What are you talking about?
Rick: (spills alcohol on Morty's bed) Come on, I got a surprise for you. (drags Morty by the ankle) Come on, hurry up. (pulls Morty out of his bed and into the hall)
Morty: Ow! Ow! You're tugging me too hard!
Rick: We gotta go, gotta get outta here, come on. Got a surprise for you Morty.
"""

@app.get('/story/stream',response_class=StreamingResponse)
async def stream_story()->AsyncIterable[str]: #tips:流式传输二进制数据时,实际上不需要声明返回类型注解
    for line in messages.splitlines():
        yield line


#tips:或者可以使用普通的def函数(不带async),并以同样的方式使用yield

@app.get('/story/stream-no-async',response_class=StreamingResponse)
def stream_no_async()->Iterable[str]:
    for line in messages.splitlines():
        yield line


"""
@app.get('/story/stream', response_class=StreamingResponse)
async def stream_story():  # tips:流式传输二进制数据时,实际上不需要声明返回类型注解
    for line in messages.splitlines():
        yield line"""

#流式输出字节
# tips:主要使用场景之一是流式输出bytes而非字符串
@app.get('/story/stream-bytes',response_class=StreamingResponse)
async def stream_story_bytes()->AsyncIterable[bytes]:
    for line in messages.splitlines():
        yield line.encode('utf-8')


#流式输出字符
@app.get('/chat/stream',response_class=StreamingResponse)
async def chat_stream():
    response_text=messages.strip()
    for char in response_text:
        yield char.encode('utf-8') #tips:关键!必须encode成bytes

        await asyncio.sleep(0.03)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
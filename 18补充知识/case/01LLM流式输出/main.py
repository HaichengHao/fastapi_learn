"""
@File    :main.py
@Editor  : 百年
@Date    :2026/6/4 11:51 
"""


from langchain.chat_models import init_chat_model
from fastapi import FastAPI,Query
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
import uvicorn
import os
load_dotenv()


#初始化大模型
llm = init_chat_model(
    model='glm-4.7',
    model_provider='openai',
    api_key=os.getenv('API_KEY'),
    base_url=os.getenv('BASE_URL')
)

#定义app

app = FastAPI(
    description='测试大模型流式输出',
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

prompt=ChatPromptTemplate(
    [
        ('system','你现在是一名律师'),

        ('human','{user_input}')
    ]
)
parser=StrOutputParser()

chain=prompt|llm|parser

@app.get('/chat/stream')
async def chat_stream(user_input:str=Query(default='你好')):
    async def event_generator():
        #构造prompt(可替换为更复杂的chain)


        async for chunk in chain.astream({
            'user_input': user_input
        }):
            if chunk:
                yield chunk.encode('utf-8')

    return StreamingResponse(event_generator(), media_type='text/plain')

if __name__ == '__main__':

    uvicorn.run(app, host='127.0.0.1', port=8848)


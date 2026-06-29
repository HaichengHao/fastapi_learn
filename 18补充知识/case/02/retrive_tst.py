"""
@File    :retrive_tst.py
@Editor  : 百年
@Date    :2026/6/29 9:44 
"""
'''
分步
加载向量数据
构建提示词
构建ragchain
利用redis-stack-server做历史记录
用gradio做可视化
'''
import gradio as gr
from langchain_core.output_parsers import StrOutputParser
from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory, RunnableConfig
from langchain_community.embeddings.dashscope import DashScopeEmbeddings
from pathlib import Path
import os
from operator import itemgetter
from loguru import logger
import asyncio
import uuid  # important:准备实现会话隔离

load_dotenv()
api_key = os.getenv('QWEN_KEY')
base_url = os.getenv('QWEN_URL')


SRC_PATH = Path(__file__).resolve().parents[1]
CHROMA_DIR = SRC_PATH / "storage" / "chroma_erp_help_db"
COLLECTION_NAME = "erp_help_docs"
REDIS_URL=os.getenv('REDIS_URL')

# =========================================================
# 1. 定义 DashScope Embedding 模型
# =========================================================

def embed_model(model_name: str | None = None) -> Embeddings:
    """
    创建 DashScope Embedding 模型。

    .env 示例：
    DASHSCOPE_API_KEY=你的key
    DASHSCOPE_EMBEDDING_MODEL=text-embedding-v4
    """

    dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")

    if not dashscope_api_key:
        raise ValueError("DASHSCOPE_API_KEY 未配置，请在 .env 中添加 DASHSCOPE_API_KEY")

    if model_name is None:
        model_name = os.getenv("DASHSCOPE_EMBEDDING_MODEL", "text-embedding-v4")

    logger.info(f"当前使用的 Embedding 模型: {model_name}")

    return DashScopeEmbeddings(
        model=model_name,
        dashscope_api_key=dashscope_api_key,
    )

# =========================================================
# 2. 加载向量数据
# ========================================================
chroma_store = Chroma(
    collection_name=COLLECTION_NAME,
    persist_directory=str(CHROMA_DIR),
    embedding_function=embed_model(),
)
retriever = chroma_store.as_retriever(search_kwargs={'k': 3})


# =========================================================
# 3. 加载对话模型
# ========================================================
llm = ChatOpenAI(
    model='qwen3.6-plus-2026-04-02',
    api_key=api_key,
    base_url=base_url,
    temperature=0.2,
    max_retries=2
)

# =========================================================
# 4. 构建提示词模板
# ========================================================

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一名ERP系统操作助手，专门回答销售合同模块相关问题。"
            "你必须严格根据【上下文】回答，不允许编造系统中不存在的按钮、流程、审批人或规则。"
            "如果上下文中没有找到相关说明，请回答：帮助文档中没有找到相关说明。"
        ),
        (
            "system",
            "【上下文】\n{context}"
        ),
        MessagesPlaceholder(variable_name="history"),
        (
            "human",
            "{user_quiz}"
        )
    ]
)


def format_docs(docs):
    return "\n\n".join(
        [
            f"【来源】{doc.metadata.get('source', '')}\n"
            f"【章节】{doc.metadata.get('section', '')}\n"
            f"【小节】{doc.metadata.get('sub_section', '')}\n"
            f"【内容】\n{doc.page_content}"
            for doc in docs
        ]
    )

# =========================================================
# 5.构建ragchain
# ========================================================
rag_chain = (
        {
            "context": itemgetter('user_quiz') | retriever | format_docs,
            'user_quiz': itemgetter('user_quiz'),
            'history': itemgetter('history')
        }
        | prompt_template
        | llm
        | StrOutputParser()
)

# =========================================================
# 6. 实现记忆功能
# ========================================================

def generate_session_id():
    return str(uuid.uuid4())


def get_session_history(session_id):
    return RedisChatMessageHistory(
        session_id=session_id,
        url=REDIS_URL,
        ttl=1200

    )

# =========================================================
# 7. 构建记忆链
# ========================================================
chain_with_history = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key='user_quiz',
    history_messages_key='history'
)


async def predict_aysnc(message, history, request: gr.Request):
    session_id = request.session_hash  # tips:做不同用户之间的隔离
    config_runnable = RunnableConfig(
        configurable={
            'session_id': session_id
        }
    )
    full_response = ''
    async for chunk in chain_with_history.astream(
            input={'user_quiz': message}, config=config_runnable

    ):
        full_response += chunk
        await asyncio.sleep(0.01)
        yield full_response


if __name__ == '__main__':
    demo = gr.ChatInterface(
        fn=predict_aysnc,
        title='ERP_AI助手',
        description='遇到ERP使用不清晰的地方请提问',
        examples=[
            "销售合同审批链怎么走？?",
            "销售合同怎么新增?",
            "给我一个合同审批流程图。"
        ],
        multimodal=False,
        autofocus=True,
    )

    demo.launch(
        server_name="127.0.0.1",
        server_port=6446,
        share=False,
        debug=True,
        theme=gr.themes.Soft()
    )

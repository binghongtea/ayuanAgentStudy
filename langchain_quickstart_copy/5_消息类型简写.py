from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

# 1.创建模型客户端
llm = ChatOpenAI(
    model="qwen3.8-max",
    base_url="https://llm-59ddchtzu57pyk9x.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    streaming=True # 看版本！
)

# 2. 准备上下文
chat_history = [
    ("system", "背景设定：你现在是一个AI老师，负责上AI课程。"),
    ("human", "你是谁?")
    # SystemMessage(content="背景设定：你现在是一个AI老师，负责上AI课程。"),
    # HumanMessage(content="你是谁?")
]

# 3.携带上下文去调用模型
result= llm.stream(input=chat_history)

# 4.处理输出
for chunk in result:
    print(chunk.content, end='', flush=True)

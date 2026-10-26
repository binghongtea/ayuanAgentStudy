from langchain_community.chat_models import ChatTongyi
from langchain_community.chat_models.openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

#1.创建模型客户端
llm = ChatOpenAI(model="qwen3.8-max",base_url="https://llm-59ddchtzu57pyk9x.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")

#2.提供上下文
chat_history = [
    SystemMessage(content="你是个ai应用助手"),
    HumanMessage(content="你是谁？")
]

#3.调用模型
result = llm.invoke(input=chat_history)

#4.处理结果
print(type(result))
print(result)
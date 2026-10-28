from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from yaml import full_load

# 1. 创建对话提示词模板
# 用用简写模式可以识别占位符，SystemMessage这种不能识别占位符
chat_prompt_template = ChatPromptTemplate.from_messages([
    ('system','假设你是一个{export}专家'),
    MessagesPlaceholder("history"),
    ('human','前一个问题我问了什么？')
])

# 2. 消息列表

chat_history = [
    ('human','LangGraph是什么？'),
    ('ai','LangGraph是一种状态管理框架，三个核心是State,Node,Edge')
]
print(chat_prompt_template.invoke({'export':'ai','content':'LangGraph','history':chat_history}).to_string())
# 3. 创建模型客户端

llm = ChatOpenAI(model="qwen3.8-max",base_url="https://llm-59ddchtzu57pyk9x.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")

# 4. 组装成LCEL表达式

chain = chat_prompt_template | llm

# 5. 调用模型

stream = chain.stream({'export':'ai','content':'LangGraph','history':chat_history})

# 6.处理输出

for chunk in stream:
    print(chunk.content,end='',flush=True)

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from yaml import full_load

# 1. 创建聊天提示词模板
# 用用简写模式可以识别占位符，SystemMessage这种不能识别占位符
chat_prompt_template = ChatPromptTemplate.from_messages([
    ('system','假设你是一个{export}专家'),
    ('human','请解释{content}是什么')
])

# prompt_template = chat_prompt_template.format(export = "ai",content = 'LangGraph')
# print(prompt_template)
# prompt_template = chat_prompt_template.invoke(input={'export':'ai','content':'LangGraph'}).to_string()
# PromptValue类型
# print(type(prompt_template))
# print(prompt_template)

# 2. 创建模型客户端

llm = ChatOpenAI(model="qwen3.8-max",base_url="https://llm-59ddchtzu57pyk9x.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")

# 3. 组装成LCEL表达式

chain = chat_prompt_template | llm

# 4. 调用模型

stream = chain.stream({'export':'ai','content':'LangGraph'})

# 5.处理输出

for chunk in stream:
    print(chunk.content,end='',flush=True)

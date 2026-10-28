from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


# 1.创建模型客户端
llm = ChatOpenAI(model="qwen3.8-max",base_url="https://llm-59ddchtzu57pyk9x.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")

# 2.创建提示词模板
prompt_template = PromptTemplate.from_template("你是个{export}专家，说明{content}是什么")

# 3.LCEL表达式
chain = prompt_template | llm

# 4.调用模型
stream = chain.stream(input={'export' : 'ai', 'content' : 'LangGraph'})

for chunk in stream:
    print(chunk.content,end='',flush=True)
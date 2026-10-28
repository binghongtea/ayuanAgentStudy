from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="qwen3.8-max",base_url="https://llm-59ddchtzu57pyk9x.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")

prompt_template = PromptTemplate.from_template(
    "假如你是一个{export},请你对{thing}是什么。"
)

user_input = prompt_template.format(export="ai专家",thing="langgragh")
print(user_input)
print(type(user_input))
stream = llm.stream(input=user_input)

for chunk in stream:
    print(chunk.content,end="",flush=True)
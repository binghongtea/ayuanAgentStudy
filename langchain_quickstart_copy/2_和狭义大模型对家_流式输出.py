from langchain_community.llms.tongyi import Tongyi

llm = Tongyi(model='qwen-max')

# 返回一个文本生成器
result = llm.stream(input="你是谁？")

for chunk in result:
    print(chunk,end='',flush=True)
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model='qwen3.8-max',base_url='https://llm-59ddchtzu57pyk9x.cn-beijing.maas.aliyuncs.com/compatible-mode/v1')

user_input = "假如你是一个{export},请你对{thing}进行解析。".format(export = 'ai专家',thing="langgragh")
print(user_input)
stream = llm.stream(input=user_input)

for chunk in stream:
    print(chunk.content,end="",flush=True)
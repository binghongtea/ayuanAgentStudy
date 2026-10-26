from openai import OpenAI

#1.创建客户端
client = OpenAI(
    base_url="https://llm-59ddchtzu57pyk9x.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

#创建消息队列
chat_history = []

#用户第一次输入
user_message1="我是楷哥，一个ai应用开发工程师"
chat_history.append({"role":"user","content":user_message1})

#第一次调用llm
completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=chat_history,
)

chat_history.append({"role":"assistant","content":completion.choices[0].message.content})

#用户第二次输入
user_message2="我是谁？"
chat_history.append({"role":"user","content":user_message2})

#第二次调用llm
completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=chat_history,
)
print(chat_history)
print()
print(completion.choices[0].message.content)
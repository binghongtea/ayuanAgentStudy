from openai import OpenAI

client = OpenAI(
    base_url="https://llm-59ddchtzu57pyk9x.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[{
        "role":"user",
        "content":"你好，我是楷哥，是一名ai应用开发工程师"
    }]
)
print('第一次调用:')

print(completion.choices[0].message.content)

completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[{
        "role":"user",
        "content":"我是谁？"
    }]
)
print('第二次调用')

print(completion.choices[0].message.content)

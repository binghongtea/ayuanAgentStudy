from openai import OpenAI

client = OpenAI(
    base_url="https://llm-59ddchtzu57pyk9x.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[
        {"role":"system","content":"背景设定：你是个ai应用开发工程师"},
        {
            "role":"user",
            "content":"你是谁？"
        }
    ]
)

print(completion.choices[0].message.content)

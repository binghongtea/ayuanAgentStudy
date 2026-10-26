from openai import OpenAI

client = OpenAI(
    base_url="https://llm-59ddchtzu57pyk9x.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[
        {
            "role":"user",
            "content":"你是谁？"
        }
    ]
)

print(completion.model_dump_json())
print(completion.choices[0].message.content)

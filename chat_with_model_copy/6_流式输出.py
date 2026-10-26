from openai import OpenAI

client = OpenAI(
    base_url="https://llm-59ddchtzu57pyk9x.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[
        {
            "role":"user",
            "content":"你是谁？详细一点"
        }
    ],
    stream= True,
    stream_options={"include_usage":True}
)

for chunk in completion:
    # print(chunk.model_dump_json())
    if chunk.choices:
        content = chunk.choices[0].delta.content
        if content:
            print(content,end='',flush=True)
    elif hasattr(chunk, "usage") and chunk.usage:
        print(f"\n本轮对话用量{chunk.usage.total_tokens}tokens")
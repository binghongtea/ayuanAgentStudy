#少样本提示词模板 fewshotTemplate
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_openai import ChatOpenAI

# 1.定义示例
examples = [
    {'input': '美丽', 'output': '漂亮'},
    {'input': '舒服', 'output': '巴适'},
]

# 2.定义实例格式化模板
example_prompt = PromptTemplate.from_template("输出：{input},输出{output}")

# 3.创建少样本提示词模板

few_shot_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="请参考以下格式，输出相应的值。",
    suffix="请直接输出答案。用户输入为{word}，输出：",
    input_variables=["word"]
)

prompt_template = few_shot_template.format(word="晴朗")
print(prompt_template)
prompt_template = few_shot_template.invoke(input={'word' : "晴朗"})
print(prompt_template)
print(prompt_template.text)
print(prompt_template.to_string())

# 4.创建模型客户端

llm = ChatOpenAI(model='qwen3.8-max',base_url="https://llm-59ddchtzu57pyk9x.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")

# 5.LCEL表达式
chain = few_shot_template | llm

# 6.调用模型

result = chain.invoke(input={"word":"晴朗"})

print(result.content)
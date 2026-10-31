from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 1.创建提示词模板

chat_prompt_template = ChatPromptTemplate([
    ('system', '假设你是ai专家'),
    ('human', '解释下{content}是什么')
]
)

# 2. 创建模型客户端

llm = ChatOpenAI(
    model='qwen3.8-max',
    base_url='https://llm-59ddchtzu57pyk9x.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
)

# 3. 创建字符串输出解析器,瓶装在LCEL末尾，将llm的输出结果都解析为Text文本

parser = StrOutputParser()

# 4. 组装LCEL表达式

chain = chat_prompt_template | llm | parser

# 5.调用大模型

# result = chain.invoke(input={'content': 'function calling'})
# print(result)
# print(type(result))

result = chain.stream(input={
    'content': 'function calling'
})

for chunk in result:
    print(chunk,end='',flush=True)


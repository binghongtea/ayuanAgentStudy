from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 创建解析器
parser = JsonOutputParser()
# 定义提示词模板，要求模型输出JSON格式
prompt = ChatPromptTemplate([
   ("human", """
    请从下面的描述中提取图书信息，只输出JSON，不要添加解释：
    {description}
    解析为JSON格式：
        {{
            "name": "书名",
            "author": "作者",
            "time": "发布时间"
        }}
    """)
])

llm = ChatOpenAI(
    model='qwen3.8-max',
    base_url='https://llm-59ddchtzu57pyk9x.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
)


chain = prompt | llm | parser

result = chain.invoke({"description": "《三体》是刘慈欣创作的科幻小说，于2008年首次出版。"})
print(result) # 例如：{'name': '三体', 'author': '刘慈欣', 'time': '2008年'}
print(type(result)) # <class 'dict'>

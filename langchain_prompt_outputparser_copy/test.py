from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

prompt_template1 = PromptTemplate.from_template("""
    请将以下内容解析为JSON格式：
    {content}
    输出格式为：{{
        "name":"",
        "author":""
    }}
""")

json_parser = JsonOutputParser()

llm = ChatOpenAI(model="qwen3.8-max",base_url="https://llm-59ddchtzu57pyk9x.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")

prompt_template2 = PromptTemplate.from_template("""
    请将以下内容翻译为英文:
    name:{name},
    author:{author}
""")

str_parser = StrOutputParser()

chain = prompt_template1 | llm | json_parser | prompt_template2 | llm | str_parser

print(chain.invoke({"content":"三体的作者是刘慈欣"}))


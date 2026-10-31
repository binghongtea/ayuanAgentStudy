from typing import Dict, List

from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

# 会话存储管理类
# 存储每个对话的历史消息
_session_store: Dict[str, BaseChatMessageHistory] = {}

class Memory:
    """
        对项目中的对话进行对话隔离，通过session_id区分
    """
    def __init__(self, session_id: str):
        self.session_id = session_id

    def get_session_history(self) -> BaseChatMessageHistory:
        # 如果有这个对话id，就返回已有对话历史，如果没有就创建一个新的空间
        if self.session_id not in _session_store:
            _session_store[self.session_id] = InMemoryChatMessageHistory()
        return _session_store[self.session_id]

    def add_human_message(self, content: str | HumanMessage):
        if isinstance(content, HumanMessage):
            self.get_session_history().add_message(content)
        else :
            self.get_session_history().add_message(HumanMessage(content))

    def add_ai_message(self, content: str | AIMessage):
        if isinstance(content, AIMessage):
            self.get_session_history().add_message(content)
        else :
            self.get_session_history().add_message(AIMessage(content))

    def messages(self) -> List[BaseMessage]:
        #BaseChatMessageHistory内有个messages的属性，类型是List[BaseMessage]
        return self.get_session_history().messages

# 对话类
class Chat:

    def __init__(self, session_id: str, system_prompt: str = "你是一个友善的AI助手，回答的结束都带一个笑脸😊。"):
        #初始化
        self.session_id = session_id
        if system_prompt:
            self.system_prompt = system_prompt

        # 创建聊天提示词模板
        chat_template_prompt = ChatPromptTemplate.from_messages([
            ('system', self.system_prompt),
            MessagesPlaceholder('history'),
            ('human', '{user_input}')
        ])

        # 创建模型客户端
        llm = ChatOpenAI(model='qwen3.8-max',base_url='https://llm-59ddchtzu57pyk9x.cn-beijing.maas.aliyuncs.com/compatible-mode/v1')

        # 字符串输出解析器
        str_parser = StrOutputParser()

        # 组装LCEL成执行链
        self.chain = chat_template_prompt | llm | str_parser

    def send(self,user_input:str):
        # 提取历史对话
        self.memory = Memory(session_id=self.session_id)

        # 实现滑动窗口
        chat_history = slidingWindow(self.memory.messages(), 1)
        print(chat_history)

        # 调用执行链
        stream = self.chain.stream(input={
            'history':chat_history,
            'user_input':user_input
        })

        full_reply = ''
        for chunk in stream:
            full_reply += chunk
            yield chunk

        self.memory.add_human_message(user_input)
        self.memory.add_ai_message(full_reply)

# 滑动窗口，截取近期n轮对话，也就是短期记忆工作记忆
def slidingWindow(messages: List[BaseMessage], size: int):
    if size * 2 > len(messages):
        return messages
    else:
        return messages[-2 * size:]

if __name__ == '__main__':
    # 创建对话类
    chat = Chat("chat_01")
    stream = chat.send('我是楷哥！')
    for chunk in stream:
        print(chunk, end='', flush=True)

    print('')

    stream = chat.send('我是谁？')
    for chunk in stream:
        print(chunk, end='', flush=True)
    print('')

    chat2 = Chat("chat_02")
    stream = chat2.send('我是谁？')
    for chunk in stream:
        print(chunk, end='', flush=True)
    print('')

    stream = chat.send('我是楷哥吗？')
    for chunk in stream:
        print(chunk, end='', flush=True)

    print('')

    stream = chat.send('我是楷哥吗？')
    for chunk in stream:
        print(chunk, end='', flush=True)

    print('')

    stream = chat.send('我是楷哥吗？')
    for chunk in stream:
        print(chunk, end='', flush=True)






































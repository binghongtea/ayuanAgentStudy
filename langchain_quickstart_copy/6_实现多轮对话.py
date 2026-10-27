from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI


class MultiTurnChat:
    """
    用langchain实现多轮对话
    """

    def __init__(self, model: str, base_url: str, system_message: str = None):
        self.model = model
        self.base_url = base_url
        # 对话列表
        self.history = []
        if system_message:
            self.history.append(SystemMessage(system_message))

        # 创建模型客户端
        self.llm = ChatOpenAI(
            model=self.model,
            base_url=self.base_url,
            streaming=True,
        )

    def add_user_message(self, content: str):
        self.history.append(HumanMessage(content))

    def add_ai_message(self, content: str):
        self.history.append(('ai', content))

    def send(self, user_input: str):
        """
        用户提供问题
        问题加入消息队列
        提取消息队列调用模型
        处理输出
        """
        self.add_user_message(user_input)

        stream = self.llm.stream(input=self.history)

        full_reply = ''
        for chunk in stream:
            if chunk.content:
                full_reply += chunk.content
                yield chunk.content

        self.add_ai_message(full_reply)

    def get_history(self):
        return self.history.copy()


if __name__ == '__main__':
    MODEL = 'qwen3.8-max'
    BASE_URL = 'https://llm-59ddchtzu57pyk9x.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
    SYSTEM_MESSAGE = '你是一个ai老师'

    chat = MultiTurnChat(model=MODEL, base_url=BASE_URL, system_message=SYSTEM_MESSAGE)

    while True:
        user_input = input('human:')
        if user_input.strip() in ['exit', 'quit']:
            print('退出系统成功')
            print(chat.get_history())
            break

        if not user_input.strip():
            print('输入不能为空')
            continue

        stream = chat.send(user_input)
        print('ai老师：', end='', flush=True)
        for chunk in stream:
            print(chunk, end='', flush=True)

        print('')

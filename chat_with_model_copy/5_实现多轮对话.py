from openai import OpenAI

class MultiTurnChat:
    """
    多轮对话用例
    """
    def __init__(self,base_url: str, model: str, system_message: str=""):
        self.base_url = base_url
        self.model = model
        self.chat_history = []
        if system_message:
            self.chat_history.append({"role":"system","content":system_message})

        # 创建客户端
        self.client = OpenAI(
            base_url=base_url,
        )

    def add_user_message(self,user_input: str) -> None:
        self.chat_history.append({"role":"user","content":user_input})

    def add_assistant_message(self,assistant_input: str) -> None:
        self.chat_history.append({"role":"assistant","content":assistant_input})

    def send_message(self,user_input: str) -> str:
        """
        1.用户输入加入队列
        2.调用llm
        3.拿到结果，加入队列
        4.返回结果
        """
        self.add_user_message(user_input)
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.chat_history,
        )
        reply = completion.choices[0].message.content
        self.add_assistant_message(reply)
        return reply


if __name__ == "__main__":

    BASE_URL = "https://llm-59ddchtzu57pyk9x.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    MODEL = "qwen3.8-max"
    SYSTEM_MESSAGE = "背景设定：你是一个很了解ai的资深ai应用开发工程师，回复前缀都带着“从专业角度看”这几个字"

    # 创建多轮对话实例
    chat = MultiTurnChat(
        base_url=BASE_URL,
        model=MODEL,
        system_message=SYSTEM_MESSAGE
    )

    print("请输入你要对ai询问的问题，输入“exit“或”quit”会自动推出对话~")

    while True:
        user_input = input("user输入：")

        #检测输入

        if user_input.lower() in ["exit","quit"]:
            print("退出多轮对话~")
            break

        if not user_input.strip():
            print("请勿输入空格字符。 \n")
            continue

        reply = chat.send_message(user_input)
        print(f"ai回答：{reply}\n")



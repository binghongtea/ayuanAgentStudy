"""使用 create_agent + InMemorySaver 实现多轮对话。

与 3_实现多轮对话.py 对照阅读：
1. InMemorySaver 替代手写 Memory 和 _session_store。
2. thread_id 对应原来的 session_id，相同 ID 可以接着聊。
3. Agent 自动保存用户消息和 AI 回复，不需要手动追加。
4. 中间件只裁剪本次模型输入，保留完整的会话状态。

InMemorySaver 只保存在当前进程的内存中，重启程序后历史会消失。
继续使用原示例的模型地址和 OPENAI_API_KEY 环境变量。
"""

from collections.abc import Callable, Iterator

from langchain.agents import create_agent
from langchain.agents.middleware import ModelRequest, ModelResponse, wrap_model_call
from langchain_core.messages import BaseMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver


# 所有 Chat 实例共享同一个 checkpointer，再通过 thread_id 隔离会话。
# 如果每次 send() 都新建 InMemorySaver，就无法读取上次的对话。
_checkpointer = InMemorySaver()


def sliding_window_middleware(size: int | None):
    """保留最近 size 轮历史；None 表示使用完整历史，0 表示只发送当前问题。

    本示例 tools=[]，每轮只有一条用户消息和一条 AI 消息。
    如果以后加入工具调用，需要另外处理工具消息的配对，不能直接按条数截取。
    """
    if size is not None and size < 0:
        raise ValueError("窗口大小不能小于 0")

    @wrap_model_call
    def sliding_window(
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        if size is None:
            return handler(request)

        # 此时 request.messages 已包含当前用户问题，所以需要加 1。
        # size=1：上一轮 human + ai + 当前 human，共最多 3 条。
        recent_messages = request.messages[-(size * 2 + 1):]

        # system_prompt 由 Agent 单独管理，不会在这里被裁掉。
        # override 只改变本次请求，不删除 checkpointer 中的完整历史。
        return handler(request.override(messages=recent_messages))

    return sliding_window


class Chat:
    def __init__(
        self,
        session_id: str,
        system_prompt: str = "你是一个友善的AI助手，回答的结束都带一个笑脸😊。",
        window_size: int | None = 1,
    ):
        self.session_id = session_id
        self.config: RunnableConfig = {
            "configurable": {"thread_id": session_id},
        }

        llm = ChatOpenAI(
            model="qwen3.8-max",
            base_url="https://llm-59ddchtzu57pyk9x.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            timeout=30,
            max_retries=1,
        )

        self.agent = create_agent(
            model=llm,
            tools=[],  # 这里只做普通聊天，暂时不添加工具。
            system_prompt=system_prompt,
            middleware=[sliding_window_middleware(window_size)],
            checkpointer=_checkpointer,
        )

    def send(self, user_input: str) -> Iterator[str]:
        # 每次只传新问题，Agent 会根据 thread_id 自动加载已有历史。
        # 如果同时把完整历史再传一次，会造成消息重复。
        stream = self.agent.stream(
            {"messages": [{"role": "user", "content": user_input}]},
            config=self.config,
            stream_mode="messages",
            version="v1",  # v1 输出 (消息片段, 元数据) 元组。
        )

        for chunk, _metadata in stream:
            # text 只提取可显示的文字，不需要再接 StrOutputParser。
            if chunk.text:
                yield chunk.text

        # 必须消费完整个 stream，才能确保这轮执行完成、状态保存完成。
        # 不要在这里再次手动添加 human / ai 消息。

    def messages(self) -> list[BaseMessage]:
        """读取当前会话保存的完整历史；这是普通方法，调用时写 messages()。"""
        state = self.agent.get_state(self.config)
        return list(state.values.get("messages", []))


if __name__ == "__main__":
    chat = Chat("chat_01", window_size=1)
    chat2 = Chat("chat_02", window_size=1)

    examples = [
        (chat, "我是楷哥！"),
        (chat, "我是谁？"),
        (chat2, "我是谁？"),  # 新会话，不应知道 chat_01 中的姓名。
        (Chat("chat_01"), "我们刚才聊了什么？"),  # 新对象、相同 ID，继续原会话。
    ]

    for current_chat, question in examples:
        print(f"\n[{current_chat.session_id}] 用户：{question}")
        print("AI：", end="", flush=True)
        for text in current_chat.send(question):
            print(text, end="", flush=True)
        print()

    # 即使 window_size=1，checkpointer 里仍保留所有轮次。
    print(f"\nchat_01 已保存 {len(chat.messages())} 条消息")
    print(f"chat_02 已保存 {len(chat2.messages())} 条消息")

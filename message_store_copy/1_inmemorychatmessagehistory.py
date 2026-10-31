from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage

memory = InMemoryChatMessageHistory()

memory.add_message(AIMessage(content="我是ai"))
memory.add_message(HumanMessage(content="请你回答1+34是多少"))


print(memory)
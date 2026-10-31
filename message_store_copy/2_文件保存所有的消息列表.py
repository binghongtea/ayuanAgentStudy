from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage

memory = FileChatMessageHistory("contact.txt")

memory.add_messages([
    AIMessage(content="1111"),
    HumanMessage(content="2222"),
])

print(memory)
from agent import hotel_agent
import uuid
from langchain_core.messages import HumanMessage, AIMessage

def chat_cli():
    print("Hotel Room Service Agent Started\n")
    session_id = str(uuid.uuid4())
    conversation = []

    while True:
        msg = input("You: ").strip()
        if msg.lower() in ["exit","quit"]: break

        conversation.append(HumanMessage(content=msg))
        result = hotel_agent.invoke({"messages": conversation}, config={"configurable": {"thread_id": session_id}})
        reply = result["messages"][-1].content
        print("\nAssistant:", reply, "\n")
        conversation.append(AIMessage(content=reply))

if __name__ == "__main__":
    chat_cli()

# agent.py
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from db.client import guests_new
from tools.new_menu_tool import get_menu
from tools.order_tool import save_order, get_order_report
from prompts.system_prompt import SYSTEM_PROMPT
from tools.tools import parse_order_items_from_text, get_current_time_str
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-preview-09-2025", temperature=0.5)


# register tool functions
tools = {
    "get_menu": get_menu,
    "save_order": save_order,
    "get_order_report": get_order_report,
}

class AgentState(dict):
    messages: list
    room_number: str | None
    pending_order: dict | None

def detect_action(text):
    t = text.lower()
    if any(k in t for k in ["menu", "food", "hungry", "eat", "what do you have"]):
        return "get_menu"
    if any(k in t for k in ["starter","main","dessert","side","drink","beverage"]):
        return "get_menu"
    if any(k in t for k in ["order","i want","give me","send","take"]):
        return "save_order"
    if any(k in t for k in ["status","report","order id","track"]):
        return "get_order_report"
    return None

def detect_arguments(action, state, text):
    txt = text.lower()
    if action == "get_menu":
        mapping = {
            "starter": "starters",
            "main": "mains",
            "dessert": "dessert",
            "side": "sides",
            "drink": "drinks",
            "juice": "drinks",
            "beverage": "drinks"
        }
        for k, v in mapping.items():
            if k in txt:
                return {"category": v}
        return {}

    if action == "save_order":
        parsed = parse_order_items_from_text(text)
        return {
            "room_number": state.get("room_number"),
            "items": parsed["items"],
            "total": parsed["total"]
        }

    if action == "get_order_report":
        return {"order_id": ''.join(ch for ch in text if ch.isalnum())}

    return {}

    
def agent_node(state: AgentState):
    messages = state["messages"]
    last = messages[-1].content
    if state.get("room_number") is None:
        if last.isdigit():
            room_found = guests_new.find_one({"room_number": last})
            if room_found:
                state["room_number"] = last
                return {"messages": messages + [
                    AIMessage(content="Thank you. What would you like to order today?")
                ]}
            else:
                return {"messages": messages + [
                    AIMessage(content="Invalid room number. Please enter a room number between 100 and 810.")
                ]}
        # If not a digit, do not loop — just remind once
        if len(messages) <= 1:     # ⚠ run only on first turn
            return {"messages": messages + [
                AIMessage(content="Welcome! Please tell me your room number to begin.")
            ]}
    # 2) TOOL DETECTION
    action = detect_action(last)
    if action:
        args = detect_arguments(action, state, last)
        result = tools[action](**args)

        if action == "get_menu":
            return {"messages": messages + [AIMessage(content=result["message"])]}

        if action == "save_order":
            if not state.get("room_number"):
                return {"messages": messages + [
                    AIMessage(content="Please provide your room number before placing an order.")
                ]}
            parsed = result
            state["pending_order"] = parsed
            return {"messages": messages + [
                AIMessage(content=f"{parsed['summary']}\n\nShall I confirm this order? (yes / no)")
            ]}

        if action == "get_order_report":
            return {"messages": messages + [AIMessage(content=result["report"])]}

    # 3) CONFIRMATION (⚠ outside the action block)
    if state.get("pending_order") and last.lower() in ["yes", "y", "ok", "confirm", "sure"]:
        data = state["pending_order"]
        saved = save_order(
            room_number=state["room_number"],
            items=data["items"],
            total=data["total"],
            history=[m.content for m in state["messages"]] )
        
        state["pending_order"] = None
        return {"messages": messages + [
            AIMessage(content=f"Order confirmed!\nOrder ID: {saved['order_id']}\n"
                              f"Total: ${saved['total']}\n"
                              f"Arrival in ~{saved['eta']} minutes.\nThank you!")
        ]}

    if state.get("pending_order") and last.lower() in ["no", "cancel"]:
        state["pending_order"] = None
        return {"messages": messages + [AIMessage(content="Order cancelled. Anything else?")]}

    # 4) LLM general chat
    ...

    system = SystemMessage(content=SYSTEM_PROMPT.format(current_time=get_current_time_str()))
    reply = llm.invoke([system] + messages)
    return {"messages": messages + [AIMessage(content=reply.content)]}

# graph build
graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.set_entry_point("agent")
graph.add_edge("agent", END)
hotel_agent = graph.compile(checkpointer=MemorySaver())

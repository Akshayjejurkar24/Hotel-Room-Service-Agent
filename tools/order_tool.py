
from db.client import orders, guests_new
from datetime import datetime
import uuid

def save_order(room_number: str, items: list, total: float, history=None):
    order_id = str(uuid.uuid4())[:10]
    eta = 40 if total < 100 else 55
    
    order_doc = {
        "order_id": order_id,
        "room_number": room_number,
        "items": [i["name"] for i in items],  # save only names, or full item dict
        "items_detail": items,  # optional: keep full price/qty
        "total": total,
        "eta": eta,
        "timestamp": datetime.utcnow(),
        "status": "confirmed",
        "conversation_history": history or []
    }

    # THIS IS THE KEY LINE
    result = orders.insert_one(order_doc)
    
    # Add _id to the document so we can use it later if needed
    order_doc["_id"] = result.inserted_id

    # Also update guest history
    guests_new.update_one(
        {"room_number": room_number},
        {"$push": {"past_orders": order_doc}}
    )

    print(f"Order saved successfully! ID: {order_id}")  # Debug line

    return order_doc  
def get_order_report(order_id):
    order = orders.find_one({"order_id": order_id})
    if not order:
        return {"report": "Order not found."}
    return {"report": f"Order status:\nRoom {order['room_number']}\nItems: {', '.join(order['items'])}\nTotal: ${order['total']}"}
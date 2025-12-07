#tool.py

from datetime import datetime
import re
from db.client import menu


def parse_order_items_from_text(text: str):
    text = text.lower()
    parts = [p.strip() for p in re.split(r"\+|,|and|&", text)]

    items = []
    for part in parts:
        qty = 1
        words = part.split()

        # detect number
        if words[0].isdigit():
            qty = int(words[0])
            name = " ".join(words[1:])
        else:
            name = part

        # find item in DB
        item_doc = menu.find_one({"name": {"$regex": f"^{name.strip()}$", "$options": "i"}})
        if item_doc:
            items.append({
                "name": item_doc["name"],
                "qty": qty,
                "price": float(item_doc["price"])
            })

    total = sum(i["qty"] * i["price"] for i in items)

    return {
        "items": items,
        "total": round(total, 2),
        "summary": "\n".join([f"• {i['qty']} x {i['name']}" for i in items]) + f"\nTotal: ${round(total, 2)}"
    }

def get_current_time_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M")

from db.client import menu
from datetime import datetime

def format_item(i):
    return f"• {i['name']} — ${i['price']}"

def get_menu(category=None):
    now = datetime.now().hour
    query = {}

    if category:
        query["category"] = category

    items = list(menu.find(query, {"_id": 0}))

    # Late-night logic
    if now >= 22 and not category:
        items = [i for i in items if i.get("cold_option") or i["category"] == "dessert"]

    if not items:
        return {"message": "Sorry, no items available right now."}

    msg = "\n".join(format_item(i) for i in items)
    return {"message": f"Here is the menu:\n\n{msg}"}

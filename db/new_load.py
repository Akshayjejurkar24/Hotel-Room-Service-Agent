# db/load_rooms.py
from client import guests_new

rooms = [str(r) for r in list(range(100,111)) + list(range(200,211)) + list(range(300,311)) + list(range(400,411)) + list(range(500,511)) + list(range(600,611)) + list(range(700,711)) + list(range(800,811))]

guests_new.drop()
for r in rooms:
    guests_new.insert_one({"room_number": r, "allergies": [], "preferences": [], "past_orders": []})

print(f"Rooms inserted: {len(rooms)}")



# from client import guests_new

# rooms = []
# for floor in [1, 2, 3, 4, 5, 6, 7, 8]:
#     for num in range(0, 10):
#         room_number = f"{floor}0{num}" if floor < 10 else f"{floor}{num}"
#         rooms.append({"room_number": room_number})

# # Custom: add 808 separatelyq
# rooms.append({"room_number": "808"})

# guests_new.drop()
# guests_new.insert_many(rooms)
# print(f"{len(rooms)} rooms inserted successfully!")

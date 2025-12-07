from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI")) 
db = client["Hotel_data"] 
menu = db.menu
guests_new = db.guests_new
orders = db.orders
print("database connected ",db)
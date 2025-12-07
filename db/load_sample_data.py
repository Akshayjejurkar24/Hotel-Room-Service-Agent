#db/load_sample_data.py is load in mongodb collection 
from client import menu
from datetime import datetime
# db/seed_menu.py  →  FINAL VERSION (25 items – perfect for the assignment)
menu_items = [
    # === MAINS ===
    {"name": "Margherita Pizza", "price": 14.99, "available": True, "category": "mains", "dietary": ["vegetarian"], "ingredients": ["tomato sauce", "mozzarella", "basil"], "prep_time": 20},
    {"name": "Pepperoni Pizza", "price": 16.99, "available": True, "category": "mains", "dietary": [], "ingredients": ["pepperoni", "mozzarella", "tomato sauce"], "prep_time": 20},
    {"name": "Grilled Salmon", "price": 26.99, "available": False, "category": "mains", "dietary": ["pescatarian"], "ingredients": ["salmon", "lemon", "dill", "butter"], "prep_time": 25},
    {"name": "Ribeye Steak", "price": 38.00, "available": True, "category": "mains", "dietary": [], "ingredients": ["beef", "butter", "garlic", "rosemary"], "prep_time": 30},
    {"name": "Chicken Tikka Masala", "price": 22.99, "available": True, "category": "mains", "dietary": [], "ingredients": ["chicken", "cream", "tomato", "yogurt", "peanuts"], "prep_time": 25},
    {"name": "Vegan Thai Green Curry", "price": 19.99, "available": True, "category": "mains", "dietary": ["vegan", "gluten-free"], "ingredients": ["coconut milk", "tofu", "eggplant", "chili"], "prep_time": 20},
    {"name": "Spicy Arrabbiata Pasta", "price": 17.99, "available": True, "category": "mains", "dietary": ["vegan"], "ingredients": ["tomato", "garlic", "chili flakes"], "prep_time": 15},
    {"name": "Paneer Butter Masala", "price": 20.99, "available": True, "category": "mains", "dietary": ["vegetarian"], "ingredients": ["paneer", "cream", "cashew", "tomato"], "prep_time": 25},

    # === STARTERS ===
    {"name": "Caesar Salad", "price": 11.99, "available": True, "category": "starters", "dietary": [], "ingredients": ["romaine", "parmesan", "anchovy", "egg", "croutons"], "prep_time": 10},
    {"name": "Caprese Salad", "price": 12.99, "available": True, "category": "starters", "dietary": ["vegetarian", "gluten-free"], "ingredients": ["tomato", "mozzarella", "basil", "olive oil"], "prep_time": 8},
    {"name": "Shrimp Cocktail", "price": 16.99, "available": True, "category": "starters", "dietary": ["pescatarian", "gluten-free"], "ingredients": ["shrimp", "cocktail sauce", "lemon"], "prep_time": 5},
    {"name": "Vegan Buddha Bowl", "price": 15.99, "available": True, "category": "starters", "dietary": ["vegan", "gluten-free"], "ingredients": ["quinoa", "avocado", "chickpeas", "tahini"], "prep_time": 10},

    # === DESSERTS (always available late night) ===
    {"name": "Chocolate Lava Cake", "price": 9.99, "available": True, "category": "dessert", "dietary": ["vegetarian"], "ingredients": ["chocolate", "egg", "butter", "flour"], "prep_time": 15},
    {"name": "Tiramisu", "price": 8.99, "available": True, "category": "dessert", "dietary": ["vegetarian"], "ingredients": ["mascarpone", "coffee", "egg", "ladyfingers"], "prep_time": 5},
    {"name": "Fresh Fruit Platter", "price": 12.99, "available": True, "category": "dessert", "dietary": ["vegan", "gluten-free"], "ingredients": ["seasonal fruit"], "prep_time": 5},

    # === COLD / LATE-NIGHT ITEMS (available after 22:30) ===
    {"name": "Club Sandwich", "price": 18.99, "available": True, "category": "mains", "dietary": [], "ingredients": ["chicken", "bacon", "egg", "lettuce", "tomato", "mayo"], "cold_option": True},
    {"name": "Cheese & Charcuterie Board", "price": 24.99, "available": True, "category": "starters", "dietary": [], "ingredients": ["cheese", "cured meats", "nuts", "grapes"], "cold_option": True},
    {"name": "Smoked Salmon Bagel", "price": 17.99, "available": True, "category": "mains", "dietary": ["pescatarian"], "ingredients": ["smoked salmon", "cream cheese", "bagel", "capers"], "cold_option": True},

    # === BEVERAGES ===
    {"name": "Coca-Cola", "price": 4.50, "available": True, "category": "drinks", "dietary": ["vegan"], "ingredients": [], "cold_option": True},
    {"name": "Still Water 1L", "price": 5.00, "available": True, "category": "drinks", "dietary": ["vegan"], "ingredients": [], "cold_option": True},
    {"name": "Fresh Orange Juice", "price": 7.99, "available": True, "category": "drinks", "dietary": ["vegan", "gluten-free"], "ingredients": ["orange"], "cold_option": True},
    {"name": "Red Bull", "price": 6.99, "available": True, "category": "drinks", "dietary": ["vegan"], "ingredients": [], "cold_option": True},

    # === SIDES ===
    {"name": "Garlic Naan", "price": 4.99, "available": True, "category": "sides", "dietary": ["vegetarian"], "ingredients": ["flour", "garlic", "butter"], "prep_time": 10},
    {"name": "French Fries", "price": 6.99, "available": True, "category": "sides", "dietary": ["vegan"], "ingredients": ["potato", "oil"], "prep_time": 15},
    {"name": "Truffle Fries", "price": 9.99, "available": False, "category": "sides", "dietary": ["vegan"], "ingredients": ["potato", "truffle oil"], "prep_time": 15},
]

menu.drop()
menu.insert_many(menu_items)
print(f"Menu seeded successfully with {len(menu_items)} items! ({datetime.now().strftime('%Y-%m-%d %H:%M')})")
...existing code...
# Hotel Room Service Agent

Simple room-service agent (CLI) that reads a menu from MongoDB and accepts orders.

Overview
- CLI agent implemented with LangGraph / LangChain-style messages.
- Menu and guest/order data stored in MongoDB (database name: Hotel_data).
- Main CLI entrypoint: main.py (interactive).
- Seed script to load sample menu: db/load_sample_data.py

Repository layout (actual files)
- .env                      # optional: MONGODB_URI
- main.py                   # CLI entrypoint (interactive)
- agent.py                  # LangGraph agent definition and graph compile
- db/
  - client.py               # MongoDB client & collections (menu, guests_new, orders)
  - load_sample_data.py     # seed/load sample menu into MongoDB
- tools/
  - tools.py                # parsing, time helpers, menu helpers
  - new_menu_tool.py        # menu tool (gets menu from DB)
  - order_tool.py           # save_order / get_order_report
- prompts/
  - system_prompt.py        # system prompt template
- requirements.txt
- README.md

Quickstart (CLI)
1. Install:
   pip install -r requirements.txt

2. Configure MongoDB URI (optional)
   Create a .env file at project root with:
   MONGODB_URI=mongodb://localhost:27017/

   If MONGODB_URI is not set, client.py should default to mongodb://localhost:27017/ (ensure client.py uses os.getenv with a default).

3. Seed sample menu (run once):
   python db/load_sample_data.py

4. Run CLI:
   python main.py
   - Type your messages. Use "exit" or "quit" to stop.
   - Provide your room number once (e.g. "room number 548" or just "548").
   - Ask "menu", "dinner", "breakfast", "vegan" to view the menu.
   - Place orders like "1 Truffle Fries" or "2 Margherita Pizza".

Troubleshooting
- If you see "database connected" but the agent keeps asking for room number:
  - Ensure main.py wraps user input as HumanMessage and merges returned state keys (messages, room_number).
  - main.py should call the compiled agent via hotel_agent.invoke(...) and pass a configurable thread_id (session id) when using MemorySaver checkpointer:
    result = hotel_agent.invoke({"messages": conversation}, config={"configurable": {"thread_id": session_id}})

- If you get checkpoint/config errors:
  - Either compile the graph with a MemorySaver instance initialized with configurable keys (thread_id/checkpoint_ns/checkpoint_id), or remove the checkpointer while debugging:
    hotel_agent = graph.compile()  # no checkpointer

- If menu items are not found when ordering:
  - tools/tools.py uses case-insensitive exact matching. Use the same item names as in the seeded menu, or improve parse regex.

Notes
- This README reflects the current project layout (db/load_sample_data.py replaces db/seed_menu.py).
- For a FastAPI web server version, replace main.py with an ASGI app and run using uvicorn (not included by default).

License / Credits
- Internal project for assignment / demo.
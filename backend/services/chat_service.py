from core.gemini import generate_response
from core.mongo import chat_collection #type: ignore
from models.chat import ChatRequest

def get_user_history(user_id: str, limit=10):
    chats = chat_collection.find({"user_id": user_id}).sort("_id", -1).limit(limit)
    history = ""
    for chat in reversed(list(chats)):
        history += f"User: {chat['user_input']}\nBot: {chat['bot_reply']}\n"
    return history

def handle_chat(user_id: str, user_input: str) -> str:
    history = get_user_history(user_id)
    full_prompt = f"{history}User: {user_input}\nBot:"
    reply = generate_response(full_prompt)
    chat_collection.insert_one({
        "user_id": user_id,
        "user_input": user_input,
        "bot_reply": reply
    })
    return reply

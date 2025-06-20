from fastapi import APIRouter, HTTPException #type: ignore
from models.chat import ChatRequest, ChatResponse, NewChatRequest, SendMessageRequest, ChatSummary, ChatMessage, RenameRequest
from models.user import UserLogin, UserCreate, UserResponse
from services.user_service import authenticate_user, create_user
from services.chat_service import handle_chat
from core.mongo import chat_collection
from core.gemini import generate_response
from uuid import uuid4
from datetime import datetime
from typing import List

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    reply = handle_chat(request.user_id, request.message)
    return ChatResponse(response=reply)

@router.post("/new_chat")
def create_new_chat(request: NewChatRequest):
    chat = {
        "chat_id": str(uuid4()),
        "created_at": datetime.utcnow().isoformat(),
        "title": request.title,
        "history": []
    }

    existing_user = chat_collection.find_one({"user_id": request.user_id})
    if existing_user:
        chat_collection.update_one(
            {"user_id": request.user_id},
            {"$push": {"chats": chat}}
        )
    else:
        chat_collection.insert_one({
            "user_id": request.user_id,
            "chats": [chat]
        })

    return { "message": "New chat created", "chat_id": chat["chat_id"] }

@router.post("/send_message", response_model=ChatResponse)
def send_message(request : SendMessageRequest):
    user_doc = chat_collection.find_one({"user_id": request.user_id})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")
    
    chat = next((c for c in user_doc["chats"] if c["chat_id"] == request.chat_id), None)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    #Building prompt form history
    history = ""
    for msg in chat["history"]:
        history += f"{msg['sender'].capitalize()}: {msg['message']}\n"
    full_prompt = f"{history}User: {request.message}\nBot:"

    # Get Gemini reply
    reply = generate_response(full_prompt)

    # Add both user and bot messages
    new_messages = [
        {"sender": "user", "message": request.message, "timestamp": datetime.utcnow().isoformat()},
        {"sender": "bot", "message": reply, "timestamp": datetime.utcnow().isoformat()}
    ]

    chat_collection.update_one(
        {"user_id": request.user_id, "chats.chat_id": request.chat_id},
        {"$push": {"chats.$.history": {"$each": new_messages}}}
    )

    return ChatResponse(response=reply)

@router.get("/get_chats/{user_id}", response_model=List[ChatSummary])
def get_all_chats(user_id: str):
    user_doc = chat_collection.find_one({"user_id": user_id})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")

    chats = user_doc.get("chats", [])
    summaries = [
        ChatSummary(chat_id=c["chat_id"], title=c["title"], created_at=c["created_at"])
        for c in chats
    ]
    return summaries

@router.get("/chat/{user_id}/{chat_id}", response_model=List[ChatMessage])
def get_chat_history(user_id: str, chat_id: str):
    user_doc = chat_collection.find_one({"user_id": user_id})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")

    chat = next((c for c in user_doc["chats"] if c["chat_id"] == chat_id), None)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    return chat.get("history", [])

@router.delete("/chat/{user_id}/{chat_id}")
def delete_chat(user_id: str, chat_id: str):
    result = chat_collection.update_one(
        {"user_id": user_id},
        {"$pull": {"chats": {"chat_id": chat_id}}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Chat not found or already deleted")

    return { "message": "Chat deleted successfully" }

@router.patch("/chat/{user_id}/{chat_id}/rename")
def rename_chat(user_id: str, chat_id: str, request: RenameRequest):
    result = chat_collection.update_one(
        {"user_id": user_id, "chats.chat_id": chat_id},
        {"$set": {"chats.$.title": request.new_title}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Chat not found or title unchanged")

    return { "message": "Chat title updated" }

@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate):
    user_id = create_user(user.username, user.password)
    return UserResponse(user_id=user_id, username=user.username)

@router.post("/login", response_model=UserResponse)
def login(user: UserLogin):
    user_id = authenticate_user(user.username, user.password)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return UserResponse(user_id=user_id, username=user.username)
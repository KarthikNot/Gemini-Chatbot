from fastapi import APIRouter, HTTPException #type: ignore
from models.chat import ChatRequest, ChatResponse, NewChatRequest, SendMessageRequest, ChatSummary, ChatMessage, RenameRequest
from models.user import UserLogin, UserCreate, UserResponse
from services.user_service import authenticate_user, create_user
from services.chat_service import handle_chat
from core.mongo import chat_collection
from core.gemini import generate_response
from core.exceptions import APIException, ValidationException, AuthenticationException, NotFoundException
from core.logging import log_error, log_info
from uuid import uuid4
from datetime import datetime
from typing import List

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """Handle simple chat request"""
    try:
        reply = handle_chat(request.user_id, request.message)
        return ChatResponse(response=reply)
    except APIException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

@router.post("/new_chat")
def create_new_chat(request: NewChatRequest):
    """Create a new chat session"""
    try:
        if not request.user_id:
            raise ValidationException("User ID is required")
        
        if not request.title or len(request.title.strip()) == 0:
            request.title = "New Chat"
        
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

        log_info(f"New chat created for user {request.user_id}")
        return { "message": "New chat created", "chat_id": chat["chat_id"] }
        
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=e.message)
    except Exception as e:
        log_error(e, "create_new_chat")
        raise HTTPException(status_code=500, detail="Failed to create chat")

@router.post("/send_message", response_model=ChatResponse)
def send_message(request: SendMessageRequest):
    """Send a message in a specific chat"""
    try:
        if not request.user_id:
            raise ValidationException("User ID is required")
        
        if not request.chat_id:
            raise ValidationException("Chat ID is required")
        
        if not request.message or len(request.message.strip()) == 0:
            raise ValidationException("Message cannot be empty")
        
        user_doc = chat_collection.find_one({"user_id": request.user_id})
        if not user_doc:
            raise NotFoundException("User not found")
        
        chat = next((c for c in user_doc["chats"] if c["chat_id"] == request.chat_id), None)
        if not chat:
            raise NotFoundException("Chat not found")

        # Building prompt from history
        history = ""
        for msg in chat["history"]:
            history += f"{msg['sender'].capitalize()}: {msg['message']}\n"
        full_prompt = f"{history}User: {request.message}\nBot:"

        # Get Gemini reply
        try:
            reply = generate_response(full_prompt)
        except Exception as e:
            log_error(e, "generate_response")
            raise HTTPException(status_code=503, detail="AI service unavailable")

        # Add both user and bot messages
        new_messages = [
            {"sender": "user", "message": request.message, "timestamp": datetime.utcnow().isoformat()},
            {"sender": "bot", "message": reply, "timestamp": datetime.utcnow().isoformat()}
        ]

        chat_collection.update_one(
            {"user_id": request.user_id, "chats.chat_id": request.chat_id},
            {"$push": {"chats.$.history": {"$each": new_messages}}}
        )

        log_info(f"Message sent successfully for user {request.user_id}, chat {request.chat_id}")
        return ChatResponse(response=reply)
        
    except (ValidationException, NotFoundException) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        log_error(e, "send_message")
        raise HTTPException(status_code=500, detail="Failed to send message")

@router.get("/get_chats/{user_id}", response_model=List[ChatSummary])
def get_all_chats(user_id: str):
    """Get all chats for a user"""
    try:
        if not user_id:
            raise ValidationException("User ID is required")
        
        user_doc = chat_collection.find_one({"user_id": user_id})
        if not user_doc:
            return []
        
        chats = user_doc.get("chats", [])
        summaries = [
            ChatSummary(chat_id=c["chat_id"], title=c["title"], created_at=c["created_at"])
            for c in chats
        ]
        
        log_info(f"Retrieved {len(summaries)} chats for user {user_id}")
        return summaries
        
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=e.message)
    except Exception as e:
        log_error(e, "get_all_chats")
        raise HTTPException(status_code=500, detail="Failed to retrieve chats")

@router.get("/chat/{user_id}/{chat_id}", response_model=List[ChatMessage])
def get_chat_history(user_id: str, chat_id: str):
    """Get chat history for a specific chat"""
    try:
        if not user_id:
            raise ValidationException("User ID is required")
        
        if not chat_id:
            raise ValidationException("Chat ID is required")
        
        user_doc = chat_collection.find_one({"user_id": user_id})
        if not user_doc:
            raise NotFoundException("User not found")

        chat = next((c for c in user_doc["chats"] if c["chat_id"] == chat_id), None)
        if not chat:
            raise NotFoundException("Chat not found")

        history = chat.get("history", [])
        
        log_info(f"Retrieved {len(history)} messages for chat {chat_id}")
        return history
        
    except (ValidationException, NotFoundException) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        log_error(e, "get_chat_history")
        raise HTTPException(status_code=500, detail="Failed to retrieve chat history")

@router.delete("/chat/{user_id}/{chat_id}")
def delete_chat(user_id: str, chat_id: str):
    """Delete a specific chat"""
    try:
        if not user_id:
            raise ValidationException("User ID is required")
        
        if not chat_id:
            raise ValidationException("Chat ID is required")
        
        result = chat_collection.update_one(
            {"user_id": user_id},
            {"$pull": {"chats": {"chat_id": chat_id}}}
        )

        if result.modified_count == 0:
            raise NotFoundException("Chat not found or already deleted")

        log_info(f"Chat {chat_id} deleted successfully for user {user_id}")
        return { "message": "Chat deleted successfully" }
        
    except (ValidationException, NotFoundException) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        log_error(e, "delete_chat")
        raise HTTPException(status_code=500, detail="Failed to delete chat")

@router.patch("/chat/{user_id}/{chat_id}/rename")
def rename_chat(user_id: str, chat_id: str, request: RenameRequest):
    """Rename a chat"""
    try:
        if not user_id:
            raise ValidationException("User ID is required")
        
        if not chat_id:
            raise ValidationException("Chat ID is required")
        
        if not request.new_title or len(request.new_title.strip()) == 0:
            raise ValidationException("New title is required")
        
        result = chat_collection.update_one(
            {"user_id": user_id, "chats.chat_id": chat_id},
            {"$set": {"chats.$.title": request.new_title}}
        )

        if result.modified_count == 0:
            raise NotFoundException("Chat not found or title unchanged")

        log_info(f"Chat {chat_id} renamed to '{request.new_title}' for user {user_id}")
        return { "message": "Chat title updated" }
        
    except (ValidationException, NotFoundException) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        log_error(e, "rename_chat")
        raise HTTPException(status_code=500, detail="Failed to rename chat")

@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate):
    """User registration"""
    try:
        user_id = create_user(user.username, user.password)
        log_info(f"User registered successfully: {user.username}")
        return UserResponse(user_id=user_id, username=user.username)
    except APIException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

@router.post("/login", response_model=UserResponse)
def login(user: UserLogin):
    """User authentication"""
    try:
        user_id = authenticate_user(user.username, user.password)
        log_info(f"User logged in successfully: {user.username}")
        return UserResponse(user_id=user_id, username=user.username)
    except APIException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
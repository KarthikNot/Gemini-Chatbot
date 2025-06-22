from core.gemini import generate_response
from core.mongo import chat_collection #type: ignore
from core.exceptions import ValidationException, NotFoundException
from core.logging import log_error, log_info
from models.chat import ChatRequest

def get_user_history(user_id: str, limit=10):
    """Get user chat history"""
    try:
        if not user_id:
            raise ValidationException("User ID is required")
        
        chats = chat_collection.find({"user_id": user_id}).sort("_id", -1).limit(limit)
        history = ""
        for chat in reversed(list(chats)):
            history += f"User: {chat['user_input']}\nBot: {chat['bot_reply']}\n"
        
        return history
        
    except ValidationException:
        raise
    except Exception as e:
        log_error(e, "get_user_history")
        raise ValidationException("Failed to retrieve chat history")

def handle_chat(user_id: str, user_input: str) -> str:
    """Handle chat with basic validation and error handling"""
    try:
        # Basic validation
        if not user_id:
            raise ValidationException("User ID is required")
        
        if not user_input or len(user_input.strip()) == 0:
            raise ValidationException("Message cannot be empty")
        
        if len(user_input) > 2000:
            raise ValidationException("Message too long (max 2000 characters)")
        
        # Get conversation history
        history = get_user_history(user_id)
        full_prompt = f"{history}User: {user_input}\nBot:"
        
        # Generate AI response
        try:
            reply = generate_response(full_prompt)
        except Exception as e:
            log_error(e, "generate_response")
            raise ValidationException("Failed to generate AI response")
        
        # Store in database
        try:
            chat_collection.insert_one({
                "user_id": user_id,
                "user_input": user_input,
                "bot_reply": reply
            })
        except Exception as e:
            log_error(e, "store_chat")
            # Don't fail the request if storage fails, but log it
            pass
        
        log_info(f"Chat handled successfully for user: {user_id}")
        return reply
        
    except ValidationException:
        raise
    except Exception as e:
        log_error(e, "handle_chat")
        raise ValidationException("Failed to handle chat")

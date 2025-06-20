from pydantic import BaseModel #type: ignore

class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    response: str

class NewChatRequest(BaseModel):
    user_id: str
    title: str = "New Chat"

class SendMessageRequest(BaseModel):
    user_id: str
    chat_id: str
    message: str

class ChatSummary(BaseModel):
    chat_id: str
    title: str
    created_at: str

class ChatMessage(BaseModel):
    sender: str
    message: str
    timestamp: str

class RenameRequest(BaseModel):
    new_title: str


#This is how the chats are stored.
# { user_id: XXXXXXXXXXX 
#   chats : {
#               {
#                   chat_id: XXXXXX,
#                    created_at: creation_date
#                   chats: {all the messages and bot messages in this chat}
#               }
    # If a user choses to create a new chat then another chat dict should appear with "chat_id, created_at, chats"
# #
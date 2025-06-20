from pymongo import MongoClient #type: ignore
import os
from dotenv import load_dotenv #type: ignore

load_dotenv()
client = MongoClient(os.getenv("MONGO_API_KEY"))
db = client["Gemini_Chatbot"]
chat_collection = db["chat"]
user_collection = db["users"]
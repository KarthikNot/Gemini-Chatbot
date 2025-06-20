import os
from dotenv import load_dotenv #type: ignore

load_dotenv()

class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    MONGODB_URI: str = os.getenv("MONGO_API_KEY")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecret")

settings = Settings()
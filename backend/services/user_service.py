from core.mongo import user_collection
from bson.objectid import ObjectId #type: ignore
import bcrypt #type: ignore

def create_user(username: str, password: str):
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    result = user_collection.insert_one({"username": username, "password": hashed_pw})
    return str(result.inserted_id)

def authenticate_user(username: str, password: str):
    user = user_collection.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        return str(user["_id"])
    return None
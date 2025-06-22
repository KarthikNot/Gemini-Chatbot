from core.mongo import user_collection
from core.exceptions import ValidationException, AuthenticationException, NotFoundException
from core.logging import log_error, log_info
from bson.objectid import ObjectId #type: ignore
import bcrypt #type: ignore

def create_user(username: str, password: str) -> str:
    """Create a new user"""
    try:
        # Basic validation
        if not username or len(username) < 3:
            raise ValidationException("Username must be at least 3 characters long")
        
        if not password or len(password) < 6:
            raise ValidationException("Password must be at least 6 characters long")
        
        # Check if username already exists
        existing_user = user_collection.find_one({"username": username})
        if existing_user:
            raise ValidationException("Username already exists")
        
        # Hash password
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Insert user into database
        result = user_collection.insert_one({
            "username": username, 
            "password": hashed_pw
        })
        
        user_id = str(result.inserted_id)
        log_info(f"User created successfully: {username}")
        return user_id
        
    except ValidationException:
        raise
    except Exception as e:
        log_error(e, "create_user")
        raise ValidationException("Failed to create user")

def authenticate_user(username: str, password: str) -> str:
    """Authenticate user"""
    try:
        # Basic validation
        if not username or not password:
            raise AuthenticationException("Username and password are required")
        
        # Query database
        user = user_collection.find_one({"username": username})
        if not user:
            raise AuthenticationException("Invalid credentials")
        
        # Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), user["password"]):
            raise AuthenticationException("Invalid credentials")
        
        user_id = str(user["_id"])
        log_info(f"User authenticated successfully: {username}")
        return user_id
        
    except AuthenticationException:
        raise
    except Exception as e:
        log_error(e, "authenticate_user")
        raise AuthenticationException("Authentication failed")
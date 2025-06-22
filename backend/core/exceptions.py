class APIException(Exception):
    """Base exception class for API errors"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class ValidationException(APIException):
    """Exception for validation errors"""
    def __init__(self, message: str):
        super().__init__(message, 400)

class NotFoundException(APIException):
    """Exception for resource not found errors"""
    def __init__(self, message: str):
        super().__init__(message, 404)

class AuthenticationException(APIException):
    """Exception for authentication errors"""
    def __init__(self, message: str):
        super().__init__(message, 401) 
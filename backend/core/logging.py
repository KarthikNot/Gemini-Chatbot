import logging
import os
from datetime import datetime

def setup_logging():
    """Setup basic logging configuration"""
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/app.log'),
            logging.StreamHandler()  # Also log to console
        ]
    )
    
    # Create logger for the application
    logger = logging.getLogger('llm_chatbot')
    logger.setLevel(logging.INFO)
    
    return logger

def log_request(method: str, path: str, status_code: int, duration: float):
    """Log HTTP request details"""
    logger = logging.getLogger('llm_chatbot')
    logger.info(f"Request: {method} {path} - Status: {status_code} - Duration: {duration:.3f}s")

def log_error(error: Exception, context: str = ""):
    """Log error with context"""
    logger = logging.getLogger('llm_chatbot')
    logger.error(f"Error in {context}: {str(error)}", exc_info=True)

def log_info(message: str):
    """Log info message"""
    logger = logging.getLogger('llm_chatbot')
    logger.info(message)

def log_warning(message: str):
    """Log warning message"""
    logger = logging.getLogger('llm_chatbot')
    logger.warning(message) 
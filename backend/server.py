from fastapi import FastAPI, Request, HTTPException #type: ignore
from fastapi.middleware.cors import CORSMiddleware #type: ignore
from fastapi.responses import JSONResponse
from api.routes import router
from core.exceptions import APIException
from core.logging import setup_logging, log_request, log_error
import time
import warnings

warnings.filterwarnings('ignore')

# Setup logging
logger = setup_logging()

app = FastAPI(title="LLM Chatbot API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware to log all requests"""
    start_time = time.time()
    
    # Log request start
    logger.info(f"Request started: {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        duration = time.time() - start_time
        
        # Log request completion
        log_request(request.method, request.url.path, response.status_code, duration)
        
        return response
    except Exception as e:
        duration = time.time() - start_time
        log_error(e, f"Request {request.method} {request.url.path}")
        raise

@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    """Handle custom API exceptions"""
    log_error(exc, f"API Exception in {request.method} {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    log_error(exc, f"General Exception in {request.method} {request.url.path}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )

app.include_router(router, prefix="/api")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    logger.info("Health check requested")
    return {"status": "healthy", "message": "LLM Chatbot API is running"}

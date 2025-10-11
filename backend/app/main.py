# app/main.py

"""
Main FastAPI Application
This is the entry point of your API server.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings


# ===== CREATE FASTAPI APPLICATION =====
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="ERP Platform with P2P Financing, IoT, and ML",
    docs_url="/docs",
    redoc_url="/redoc",
)


# ===== CONFIGURE CORS =====
# CORS = Cross-Origin Resource Sharing
# This allows your Vue.js frontend (different domain) to call your API
# Without this, browsers block the requests for security
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (in production, specify your frontend domain)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===== YOUR FIRST API ENDPOINT! =====
@app.get("/")
def read_root():
    """
    Root endpoint - test if API is running.
    
    When you visit http://localhost:8000/ you'll see this response.
    
    Returns:
        Dictionary with welcome message
    """
    return {
        "message": "Welcome to ERP Platform API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    
    Used to verify the API is alive and responding.
    Useful for monitoring and deployment systems.
    
    Returns:
        Dictionary with health status
    """
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME
    }


@app.get("/api/v1/test")
def test_endpoint():
    """
    Test endpoint under /api/v1 prefix.
    
    This demonstrates the API versioning structure.
    All your future endpoints will be under /api/v1/
    
    Returns:
        Dictionary with test message
    """
    return {
        "message": "API v1 is working!",
        "endpoint": "/api/v1/test"
    }


# ===== STARTUP EVENT =====
@app.on_event("startup")
async def startup_event():
    """
    Runs when the API server starts.
    
    Use this to:
    - Initialize database connections
    - Load ML models
    - Start background tasks
    """
    print("=" * 50)
    print(f"🚀 {settings.APP_NAME} Starting...")
    print(f"📖 API Documentation: http://localhost:8000/docs")
    print(f"🔍 Alternative Docs: http://localhost:8000/redoc")
    print(f"⚡ Version: {settings.APP_VERSION}")
    print("=" * 50)


# ===== SHUTDOWN EVENT =====
@app.on_event("shutdown")
async def shutdown_event():
    """
    Runs when the API server shuts down.
    
    Use this to:
    - Close database connections
    - Save state
    - Clean up resources
    """
    print("=" * 50)
    print(f"🛑 {settings.APP_NAME} Shutting Down...")
    print("=" * 50)
# app/main.py

"""
Main FastAPI Application
This is the entry point of your API server.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.auth import router as auth_router
from app.api.company import router as company_router # Import the new company router


# ===== CREATE FASTAPI APPLICATION =====
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Islamic ERP Platform with P2P Financing, IoT, and ML",
    docs_url="/docs",
    redoc_url="/redoc",
)


# ===== CONFIGURE CORS =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===== INCLUDE ROUTERS =====
app.include_router(auth_router)
app.include_router(company_router) # Include the new company router


# ===== YOUR FIRST API ENDPOINT! =====
@app.get("/")
def read_root():
    """Root endpoint - test if API is running."""
    return {
        "message": "Welcome to Islamic ERP Platform API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME
    }


@app.get("/api/v1/test")
def test_endpoint():
    """Test endpoint under /api/v1 prefix."""
    return {
        "message": "API v1 is working!",
        "endpoint": "/api/v1/test"
    }


# ===== STARTUP EVENT =====
@app.on_event("startup")
async def startup_event():
    """Runs when the API server starts."""
    print("=" * 50)
    print(f"🚀 {settings.APP_NAME} Starting...")
    print(f"📖 API Documentation: http://localhost:8000/docs")
    print(f"🔍 Alternative Docs: http://localhost:8000/redoc")
    print(f"⚡ Version: {settings.APP_VERSION}")
    print("=" * 50)


# ===== SHUTDOWN EVENT =====
@app.on_event("shutdown")
async def shutdown_event():
    """Runs when the API server shuts down."""
    print("=" * 50)
    print(f"🛑 {settings.APP_NAME} Shutting Down...")
    print("=" * 50)

# app/core/config.py

"""
Configuration Settings
This file loads environment variables and provides them to the app.
"""

from pydantic_settings import BaseSettings  # For loading .env file
from typing import Optional  # For optional values


class Settings(BaseSettings):
    """
    Application settings loaded from .env file
    
    Pydantic automatically reads from .env file and validates the values.
    """
    
    # ===== DATABASE SETTINGS =====
    DATABASE_URL: str  # Connection string to PostgreSQL
    
    # ===== SECURITY SETTINGS =====
    SECRET_KEY: str  # Secret key for JWT token encryption
    ALGORITHM: str = "HS256"  # Algorithm for JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Token expiration time
    
    # ===== APPLICATION SETTINGS =====
    APP_NAME: str = "ERP Platform"  # Application name
    APP_VERSION: str = "1.0.0"  # Version
    DEBUG: bool = True  # Debug mode (True for development)
    
    # ===== API SETTINGS =====
    API_V1_PREFIX: str = "/api/v1"  # API URL prefix
    
    class Config:
        """
        Pydantic configuration
        Tells Pydantic to load values from .env file
        """
        env_file = ".env"  # Look for .env file in same directory as main.py
        case_sensitive = True  # Environment variables are case-sensitive


# Create a single instance of settings to use throughout the app
# This loads all values from .env when the app starts
settings = Settings()
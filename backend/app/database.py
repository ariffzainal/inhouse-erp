# app/database.py

"""
Database Connection and Session Management

This file sets up:
1. Connection to PostgreSQL
2. Session management (how we talk to the database)
3. Base class for all database models
"""

from sqlalchemy import create_engine  # Creates database connection
from sqlalchemy.ext.declarative import declarative_base  # Base class for models
from sqlalchemy.orm import sessionmaker  # Creates database sessions
from app.core.config import settings  # Import our configuration


# ===== CREATE DATABASE ENGINE =====
# The engine is like a "connection pool" to the database
# It manages connections efficiently
engine = create_engine(
    settings.DATABASE_URL,  # Connection string from .env
    pool_pre_ping=True,  # Check if connection is alive before using it
    echo=settings.DEBUG,  # Print SQL queries if DEBUG=True (helpful for learning!)
)


# ===== CREATE SESSION FACTORY =====
# A session is like a "conversation" with the database
# SessionLocal is a factory that creates new sessions
SessionLocal = sessionmaker(
    autocommit=False,  # Don't auto-save changes (we control when to save)
    autoflush=False,  # Don't auto-flush changes (we control when to flush)
    bind=engine,  # Connect sessions to our database engine
)


# ===== CREATE BASE CLASS FOR MODELS =====
# All database models (tables) will inherit from this Base class
Base = declarative_base()


# ===== DEPENDENCY FOR FASTAPI =====
def get_db():
    """
    Dependency function that provides a database session.
    
    This is used in FastAPI endpoints like this:
    @app.get("/users")
    def get_users(db: Session = Depends(get_db)):
        # db is automatically provided here!
    
    The session is automatically closed after the request finishes.
    """
    db = SessionLocal()  # Create a new session
    try:
        yield db  # Provide session to the endpoint
    finally:
        db.close()  # Always close session when done (even if error occurs)
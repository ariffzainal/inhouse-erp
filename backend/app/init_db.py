# app/init_db.py

"""
Database Initialization Script

This creates all database tables.
Run this once to set up the database schema.
"""

from app.database import engine, Base
from app.models.user import User  # Import all models here


def init_db():
    """
    Create all database tables.
    
    This looks at all models that inherit from Base
    and creates their corresponding tables in PostgreSQL.
    """
    print("Creating database tables...")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    print("✅ Database tables created successfully!")
    print(f"   - {User.__tablename__}")


if __name__ == "__main__":
    # Run this script directly to create tables
    init_db()
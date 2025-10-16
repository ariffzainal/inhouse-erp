# app/models/user.py

"""
User Model - Database Table Definition

This defines the structure of the 'users' table in PostgreSQL.
SQLAlchemy ORM converts this Python class into a database table.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum


# ===== USER ROLE ENUM =====
class UserRole(str, enum.Enum):
    """
    User roles for access control.
    
    - ADMIN: Full access to everything
    - MANAGER: Can manage employees, view reports
    - ACCOUNTANT: Access to accounting module
    - INVENTORY_STAFF: Access to inventory, can scan barcodes
    - POS_STAFF: Access to POS system
    - KITCHEN_STAFF: Access to kitchen display
    - VIEWER: Read-only access
    """
    ADMIN = "admin"
    MANAGER = "manager"
    ACCOUNTANT = "accountant"
    INVENTORY_STAFF = "inventory_staff"
    POS_STAFF = "pos_staff"
    KITCHEN_STAFF = "kitchen_staff"
    VIEWER = "viewer"


# ===== USER MODEL =====
class User(Base):
    """
    User table - stores all user accounts.
    
    This class becomes a table named 'users' in PostgreSQL.
    Each attribute becomes a column in the table.
    """
    
    # Table name in database
    __tablename__ = "users"
    
    # ===== COLUMNS =====
    
    # Primary key - unique identifier for each user
    id = Column(
        Integer,  # Data type
        primary_key=True,  # This is the primary key
        index=True,  # Create index for faster lookups
        autoincrement=True  # Automatically increment (1, 2, 3, ...)
    )
    
    # Email - must be unique (no two users can have same email)
    email = Column(
        String(255),  # Maximum 255 characters
        unique=True,  # Must be unique across all users
        index=True,  # Index for faster searches
        nullable=False  # Cannot be NULL (required field)
    )
    
    # Full name
    full_name = Column(
        String(255),
        nullable=False
    )
    
    # Hashed password (NEVER store plain text passwords!)
    hashed_password = Column(
        String(255),
        nullable=False
    )
    
    # Is account active? (for disabling users without deleting)
    is_active = Column(
        Boolean,
        default=True,  # New users are active by default
        nullable=False
    )
    
    # Is email verified? (for email verification feature - future)
    is_verified = Column(
        Boolean,
        default=False,  # Users start unverified
        nullable=False
    )
    
    # When was account created?
    created_at = Column(
        DateTime(timezone=True),  # Store with timezone
        server_default=func.now(),  # Automatically set to current time
        nullable=False
    )
    
    # When was account last updated?
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),  # Automatically update when record changes
        nullable=False
    )

    # Default company associated with the user (the one they registered with)
    default_company_id = Column(
        Integer,
        nullable=True # Can be null if user hasn't registered with a company yet
    )
    default_company_name = Column(
        String(255),
        nullable=True # Can be null if user hasn't registered with a company yet
    )
    
    # ===== STRING REPRESENTATION =====
    def __repr__(self):
        """
        How to display User object when printed.
        Useful for debugging.
        """
        return f"<User(id={self.id}, email={self.email})>"

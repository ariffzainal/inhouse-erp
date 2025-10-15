# app/schemas/user.py

"""
User Schemas - Data Validation with Pydantic

Schemas define:
- What data the API accepts (input)
- What data the API returns (output)
- Validation rules (email format, password length, etc.)
"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.user import UserRole
from app.schemas.company import CompanyRegister


# ===== BASE USER SCHEMA =====
class UserBase(BaseModel):
    """
    Base schema with common fields.
    Other schemas inherit from this.
    """
    email: EmailStr  # Validates email format automatically
    full_name: str = Field(..., min_length=2, max_length=255)  # Required, 2-255 chars


# ===== USER CREATION SCHEMA =====
class UserCreate(UserBase):
    """
    Schema for creating a new user (registration).
    
    Used in: POST /api/v1/auth/register
    
    Example request body:
    {
        "email": "user@example.com",
        "full_name": "John Doe",
        "password": "SecurePass123!",
        "role": "inventory_staff"
    }
    """
    password: str = Field(
        ...,  # Required field
        min_length=8,  # Minimum 8 characters
        max_length=100,  # Maximum 100 characters
        description="Password must be at least 8 characters"
    )

    company: CompanyRegister  # ← ADD THIS
    role: Optional[UserRole] = UserRole.VIEWER  # Optional, defaults to VIEWER


# ===== USER LOGIN SCHEMA =====
class UserLogin(BaseModel):
    """
    Schema for user login.
    
    Used in: POST /api/v1/auth/login
    
    Example request body:
    {
        "email": "user@example.com",
        "password": "SecurePass123!"
    }
    """
    email: EmailStr
    password: str


# ===== USER RESPONSE SCHEMA =====
class UserResponse(UserBase):
    """
    Schema for returning user data (what API sends back).
    
    NEVER include password in responses!
    
    Used in: All endpoints that return user data
    
    Example response:
    {
        "id": 1,
        "email": "user@example.com",
        "full_name": "John Doe",
        "role": "inventory_staff",
        "is_active": true,
        "is_verified": false,
        "created_at": "2025-01-15T10:30:00Z"
    }
    """
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    # Current company context (added when user selects company)
    current_company_id: Optional[int] = None
    current_company_name: Optional[str] = None
    current_role: Optional[str] = None # This is where the role for the current company is stored
    
    # Pydantic V2 configuration
    model_config = ConfigDict(from_attributes=True)  # Allow ORM models


# ===== TOKEN RESPONSE SCHEMA =====
class Token(BaseModel):
    """
    Schema for authentication token response.
    
    Used in: POST /api/v1/auth/login (successful login)
    
    Example response:
    {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5...",
        "token_type": "bearer"
    }
    """
    access_token: str
    token_type: str = "bearer"


# ===== TOKEN DATA SCHEMA =====
class TokenData(BaseModel):
    """
    Schema for data stored inside JWT token.
    
    The token contains the user's email.
    When we decode the token, we get this data.
    """
    email: Optional[str] = None


# ===== USER UPDATE SCHEMA =====
class UserUpdate(BaseModel):
    """
    Schema for updating user data.
    
    All fields are optional (only update what's provided).
    
    Used in: PUT /api/v1/users/me (update own profile)
    
    Example request body:
    {
        "full_name": "Jane Doe",
        "email": "newemail@example.com"
    }
    """
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=2, max_length=255)
    password: Optional[str] = Field(None, min_length=8, max_length=100)
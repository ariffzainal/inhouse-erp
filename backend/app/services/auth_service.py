# app/services/auth_service.py

"""
Authentication Service
Business logic for user authentication and management.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password, create_access_token
from app.services.company_service import create_company_with_owner


# ===== CREATE NEW USER =====
def create_user(db: Session, user_data: UserCreate) -> tuple[User, int]:
    """
    Create a new user account with company.
    
    Steps:
    1. Check if email already exists
    2. Hash the password
    3. Create user record
    4. Create company with user as owner
    5. Return user object and company_id
    
    Args:
        db: Database session
        user_data: User registration data (includes company data)
        
    Returns:
        Tuple of (User, company_id)
        
    Raises:
        HTTPException: If email already exists
    """
    
    # Check if user with this email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash the password (NEVER store plain text!)
    hashed_pwd = hash_password(user_data.password)
    
    # Create user object (WITHOUT role - role is now per-company)
    db_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_pwd,
        is_active=True,
        is_verified=False  # Will implement email verification later
    )
    
    # Add user to database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create company and assign user as owner
    company, member = create_company_with_owner(
        db=db,
        company_data=user_data.company,
        user=db_user
    )
    
    return db_user, company.id


# ===== AUTHENTICATE USER =====
def authenticate_user(db: Session, email: str, password: str) -> User:
    """
    Authenticate user with email and password.
    
    Steps:
    1. Find user by email
    2. Verify password
    3. Check if account is active
    4. Return user if valid
    
    Args:
        db: Database session
        email: User's email
        password: Plain text password from login form
        
    Returns:
        User object if authentication successful
        
    Raises:
        HTTPException: If authentication fails
    """
    
    # Find user by email
    user = db.query(User).filter(User.email == email).first()
    
    # Check if user exists
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if account is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled"
        )
    
    return user


# ===== GET USER BY EMAIL =====
def get_user_by_email(db: Session, email: str) -> User:
    """
    Retrieve user by email address.
    
    Args:
        db: Database session
        email: User's email
        
    Returns:
        User object or None if not found
    """
    return db.query(User).filter(User.email == email).first()


# ===== GET USER BY ID =====
def get_user_by_id(db: Session, user_id: int) -> User:
    """
    Retrieve user by ID.
    
    Args:
        db: Database session
        user_id: User's ID
        
    Returns:
        User object or None if not found
    """
    return db.query(User).filter(User.id == user_id).first()
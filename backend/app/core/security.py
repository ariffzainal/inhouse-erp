# app/core/security.py

"""
Security Functions
Handles password hashing and JWT token creation/verification.
"""

from datetime import datetime, timedelta  # For token expiration
from typing import Optional  # For optional parameters
from jose import JWTError, jwt  # For creating/verifying JWT tokens
from passlib.context import CryptContext  # For password hashing
from app.core.config import settings  # Import our configuration


# ===== PASSWORD HASHING =====
# CryptContext handles password encryption using bcrypt algorithm
# bcrypt is industry-standard for password hashing (very secure!)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a plain text password.
    
    Example:
        plain_password = "mypassword123"
        hashed = hash_password(plain_password)
        # Result: "$2b$12$KIXxAbC..." (irreversible hash)
    
    Args:
        password: Plain text password from user
        
    Returns:
        Hashed password string (safe to store in database)
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Example:
        is_correct = verify_password("mypassword123", stored_hash)
        # Returns: True if password matches, False otherwise
    
    Args:
        plain_password: Password user typed in login form
        hashed_password: Hashed password from database
        
    Returns:
        True if password matches, False if it doesn't
    """
    return pwd_context.verify(plain_password, hashed_password)


# ===== JWT TOKEN CREATION =====
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    JWT (JSON Web Token) is like a secure "ticket" that proves user is logged in.
    The token contains user info and expiration time, all encrypted.
    
    Example:
        token = create_access_token({"sub": "user@example.com"})
        # Returns: "eyJhbGciOiJIUzI1NiIsInR5..." (encrypted token)
    
    Args:
        data: Dictionary with user information (usually {"sub": user_email})
        expires_delta: How long token is valid (default: 30 minutes from settings)
        
    Returns:
        Encrypted JWT token string
    """
    # Make a copy of data so we don't modify original
    to_encode = data.copy()
    
    # Calculate expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Default expiration from settings (30 minutes)
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Add expiration to token data
    to_encode.update({"exp": expire})
    
    # Create encrypted token using SECRET_KEY from .env
    encoded_jwt = jwt.encode(
        to_encode,  # Data to encrypt
        settings.SECRET_KEY,  # Secret key (from .env)
        algorithm=settings.ALGORITHM  # Encryption method (HS256)
    )
    
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """
    Verify and decode a JWT token.
    
    This checks if:
    - Token is valid (not tampered with)
    - Token hasn't expired
    - Token was created with our SECRET_KEY
    
    Example:
        token_data = verify_token(token_from_user)
        if token_data:
            user_email = token_data.get("sub")
            # User is authenticated!
        else:
            # Token is invalid or expired
    
    Args:
        token: JWT token string from user's request
        
    Returns:
        Decoded token data (dict) if valid, None if invalid
    """
    try:
        # Decode the token using our SECRET_KEY
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        # Token is invalid, expired, or tampered with
        return None
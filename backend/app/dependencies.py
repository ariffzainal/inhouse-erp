from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError # Used for handling JWT token errors

from app.database import SessionLocal # Import SessionLocal to create DB sessions
from app.core.security import verify_token # Import function to verify JWT tokens
from app.models.user import User # Import the User model
from app.services import auth_service # Import auth_service to get user by email

# This tells FastAPI how to expect the token (Bearer token in Authorization header)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")

# Dependency to get a database session
def get_db():
    """
    Provides a database session for a request.
    Ensures the session is closed after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db # 'yield' makes this a context manager
    finally:
        db.close()

# Dependency to get the current authenticated user from the JWT token
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Decodes the JWT token from the request, verifies it,
    and fetches the corresponding user from the database.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Verify the token and get its payload
        payload = verify_token(token)
        email: str = payload.get("sub") # 'sub' (subject) usually holds the user's email
        if email is None:
            raise credentials_exception
    except JWTError:
        # If token is invalid or expired
        raise credentials_exception
    
    # Fetch the user from the database using the email from the token
    user = auth_service.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    
    return user

# Dependency to get the current active user (ensures user is active)
async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Ensures the authenticated user is active.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user
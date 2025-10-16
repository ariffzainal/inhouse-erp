from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError # Used for handling JWT token errors

from app.database import SessionLocal # Import SessionLocal to create DB sessions
from app.core.security import verify_token # Import function to verify JWT tokens
from app.models.user import User # Import the User model
from app.schemas.user import UserResponse # Import UserResponse schema
from app.services import auth_service # Import auth_service to get user by email
from app.services.company_service import get_company_member_role # Import to get user's role in a company

# This tells FastAPI how to expect the token (Bearer token in Authorization header)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login") # Corrected tokenUrl

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
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserResponse:
    """
    Decodes the JWT token from the request, verifies it,
    and fetches the corresponding user from the database.
    Returns a UserResponse schema with current and default company context.
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
    user_model = auth_service.get_user_by_email(db, email=email)
    if user_model is None:
        raise credentials_exception

    # Build response with company context
    response = UserResponse.model_validate(user_model)

    # If no current company is set in the response, default to the user's registered company
    if response.current_company_id is None and response.default_company_id is not None:
        response.current_company_id = response.default_company_id
        response.current_company_name = response.default_company_name
        # Note: We are updating the Pydantic response model, not the SQLAlchemy model here.
        # If we wanted to persist this change to the database, it would need to be done
        # on the user_model object and then committed. For now, this is just for the response.
    
    # Determine the current role based on the current company
    if response.current_company_id:
        response.current_role = get_company_member_role(db, user_model.id, response.current_company_id)
    
    return response

# Dependency to get the current active user (ensures user is active)
async def get_current_active_user(current_user: UserResponse = Depends(get_current_user)) -> UserResponse:
    """
    Ensures the authenticated user is active.
    """
    # Note: current_user is now UserResponse, which has is_active
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user

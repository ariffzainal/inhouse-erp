# app/api/auth.py

"""
Authentication API Endpoints
Routes for user registration, login, and token management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, Token
from app.services.auth_service import create_user, authenticate_user, get_user_by_email
from app.core.security import create_access_token, verify_token
from app.services.company_service import get_company_by_id
from app.dependencies import get_db, get_current_user
from app.services import auth_service # ← ADD THIS IMPORT
from app.services.company_service import get_company_by_id
from app.models.user import User # Import the User model


# ===== ROUTER SETUP =====
router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)


# ===== OAUTH2 SCHEME =====
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# ===== DEPENDENCY: GET CURRENT USER =====
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    Dependency to get currently authenticated user.
    Extracts and verifies JWT token, then returns user object.
    """
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = get_user_by_email(db, email=email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user


# ===== ENDPOINT: REGISTER NEW USER =====
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user account with company.
    
    User becomes company owner automatically with admin role.
    
    Request Body:
    {
        "email": "owner@company.com",
        "full_name": "John Doe",
        "password": "SecurePass123!",
        "company": {
            "display_name": "Acme Corp",
            "legal_name": "Acme Corporation Sdn Bhd",
            "business_registration_number": "202301234567"
        }
    }
    
    Response: User object with company info
    """
    user, company_id = auth_service.create_user(db, user_data)
    
    # Get company details to include in response
    company = get_company_by_id(db, company_id)
    
    # Build response with company context
    response = UserResponse.model_validate(user)
    response.current_company_id = company.id
    response.current_company_name = company.display_name
    response.current_role = "admin" # The owner of the primary company is an admin
    response.default_company_id = company.id
    response.default_company_name = company.display_name
    
    return response


# ===== ENDPOINT: LOGIN =====
@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login and receive JWT access token.
    
    Use email as username field.
    Returns access token for authentication.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# ===== ENDPOINT: GET CURRENT USER INFO =====
@router.get("/me", response_model=UserResponse)
def get_me(current_user: UserResponse = Depends(get_current_user)):
    """
    Get currently authenticated user information.
    
    Requires valid Bearer token in Authorization header.
    """
    return current_user


# ===== ENDPOINT: TEST PROTECTED ROUTE =====
@router.get("/protected")
def protected_route(current_user: UserResponse = Depends(get_current_user)):
    """
    Test endpoint to verify authentication works.
    
    Requires authentication.
    """
    return {
        "message": "This is a protected route",
        "user": current_user.email,
        "role": current_user.role
    }

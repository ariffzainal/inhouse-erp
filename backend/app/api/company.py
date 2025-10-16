from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.company import CompanyUpdate, CompanyResponse, CompanySelect # Added CompanySelect
from app.schemas.user import UserResponse # Import UserResponse
from app.dependencies import get_current_user
from app.models.user import User
from app.services.company_service import get_company_by_id, update_company, get_user_companies_detailed, set_active_company # Added set_active_company

router = APIRouter(
    prefix="/api/v1/companies",
    tags=["Companies"]
)

@router.get("/", response_model=list[CompanyResponse]) # Changed to list[CompanyResponse]
def get_my_companies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve a list of all companies the current user is a member of.
    """
    companies = get_user_companies_detailed(db, current_user.id)
    return companies

@router.put("/{company_id}", response_model=CompanyResponse)
def update_company_profile(
    company_id: int,
    company_data: CompanyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a company's profile.
    Only the company owner or an admin of that company can update its profile.
    """
    # TODO: Implement authorization logic to ensure only owner/admin can update
    # For now, we'll just check if the user is authenticated.
    
    company = get_company_by_id(db, company_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    # Placeholder for actual authorization check
    # In a real app, you'd check if current_user is an admin or owner of company_id
    # For now, we'll allow any authenticated user to update if they know the ID.
    # This needs to be strengthened.
    
    updated_company = update_company(db, company, company_data)
    return updated_company


@router.post("/select", response_model=UserResponse)
def select_company(
    company_select: CompanySelect,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Set the current active company for the authenticated user.
    """
    updated_user = set_active_company(db, current_user, company_select.company_id)
    return updated_user

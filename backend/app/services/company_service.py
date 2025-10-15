"""
Company Service
Business logic for company management.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.company import Company
from app.models.company_member import CompanyMember, MemberStatus
from app.models.user import User, UserRole
from app.schemas.company import CompanyRegister, CompanyUpdate, CompanyResponse # Added CompanyResponse
import re


def create_slug(name: str) -> str:
    """
    Create URL-friendly slug from company name.
    
    Example: "Acme Corporation Sdn Bhd" -> "acme-corporation-sdn-bhd"
    """
    # Convert to lowercase
    slug = name.lower()
    # Replace spaces with hyphens
    slug = re.sub(r'\s+', '-', slug)
    # Remove special characters except hyphens
    slug = re.sub(r'[^a-z0-9\-]', '', slug)
    # Remove multiple hyphens
    slug = re.sub(r'\-+', '-', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    return slug


def create_company_with_owner(
    db: Session, 
    company_data: CompanyRegister, 
    user: User
) -> tuple[Company, CompanyMember]:
    """
    Create a company and assign user as owner with admin role.
    
    Args:
        db: Database session
        company_data: Company registration data
        user: User who will be company owner
        
    Returns:
        Tuple of (Company, CompanyMember)
    """
    
    # Generate slug from display name
    base_slug = create_slug(company_data.display_name)
    slug = base_slug
    
    # Ensure slug is unique (add number if exists)
    counter = 1
    while db.query(Company).filter(Company.slug == slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1
    
    # Create company
    company = Company(
        display_name=company_data.display_name,
        legal_name=company_data.legal_name,
        slug=slug,
        business_registration_number=company_data.business_registration_number,
        is_active=True
    )
    
    db.add(company)
    db.flush()  # Get company.id without committing
    
    # Create company member (user as owner with admin role)
    member = CompanyMember(
        user_id=user.id,
        company_id=company.id,
        role=UserRole.ADMIN,  # Owner gets admin role
        status=MemberStatus.ACTIVE,
        is_owner=True
    )
    
    db.add(member)
    db.commit()
    db.refresh(company)
    db.refresh(member)
    
    return company, member


def get_company_by_id(db: Session, company_id: int) -> Company:
    """Get company by ID"""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    return company


def get_user_companies(db: Session, user_id: int):
    """
    Get all companies a user belongs to.
    
    Returns list of tuples: (Company, CompanyMember)
    """
    results = db.query(Company, CompanyMember).join(
        CompanyMember, 
        Company.id == CompanyMember.company_id
    ).filter(
        CompanyMember.user_id == user_id,
        CompanyMember.status == MemberStatus.ACTIVE
    ).all()
    
    return results


def get_user_companies_detailed(db: Session, user_id: int) -> list[CompanyResponse]:
    """
    Get all companies a user belongs to, returning detailed CompanyResponse objects.
    """
    results = db.query(Company, CompanyMember).join(
        CompanyMember, 
        Company.id == CompanyMember.company_id
    ).filter(
        CompanyMember.user_id == user_id,
        CompanyMember.status == MemberStatus.ACTIVE
    ).all()
    
    companies_data = []
    for company, member in results:
        company_response = CompanyResponse.model_validate(company)
        # You might want to add the user's role in this company to the CompanyResponse
        # For now, we'll just return the company details.
        companies_data.append(company_response)
        
    return companies_data


def update_company(
    db: Session, 
    company: Company, # Changed from company_id to company object
    update_data: CompanyUpdate
) -> Company:
    """
    Update company details.
    
    Args:
        db: Database session
        company_id: Company to update
        update_data: Fields to update
        
    Returns:
        Updated Company object
    """
    # Update only provided fields
    update_dict = update_data.model_dump(exclude_unset=True)
    
    # If display_name changed, regenerate slug
    if "display_name" in update_dict and update_dict["display_name"] != company.display_name:
        base_slug = create_slug(update_dict["display_name"])
        slug = base_slug
        counter = 1
        while db.query(Company).filter(
            Company.slug == slug, 
            Company.id != company.id # Use company.id here
        ).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
        update_dict["slug"] = slug
    
    # Apply updates
    for key, value in update_dict.items():
        setattr(company, key, value)
    
    db.commit()
    db.refresh(company)
    
    return company


def check_user_company_access(
    db: Session, 
    user_id: int, 
    company_id: int
) -> CompanyMember:
    """
    Check if user has access to company.
    
    Returns CompanyMember if user has access.
    Raises 403 if no access.
    """
    member = db.query(CompanyMember).filter(
        CompanyMember.user_id == user_id,
        CompanyMember.company_id == company_id,
        MemberStatus.ACTIVE
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No access to this company"
        )
    
    return member


def set_active_company(db: Session, user: User, company_id: int) -> User:
    """
    Set the active company for a user.
    
    Args:
        db: Database session
        user: The authenticated user
        company_id: The ID of the company to set as active
        
    Returns:
        The updated User object
        
    Raises:
        HTTPException: If the user does not have access to the company
    """
    member = check_user_company_access(db, user.id, company_id)
    
    user.current_company_id = company_id
    user.current_company_name = db.query(Company).filter(Company.id == company_id).first().display_name
    user.current_role = member.role.value # Store the string value of the enum
    
    db.commit()
    db.refresh(user)
    
    return user

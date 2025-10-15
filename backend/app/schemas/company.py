# app/schemas/company.py

"""
Company Schemas - Data validation for company operations
"""

from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.company import BusinessStructure, Industry


# ===== COMPANY REGISTRATION SCHEMA =====

class CompanyRegister(BaseModel):
    """Schema for company registration (required fields only)"""
    display_name: str = Field(..., min_length=2, max_length=255)
    legal_name: str = Field(..., min_length=2, max_length=255)
    business_registration_number: str = Field(..., min_length=3, max_length=100)


# ===== COMPANY UPDATE SCHEMA =====

class CompanyUpdate(BaseModel):
    """Schema for updating company details (all fields optional)"""
    
    # Basic info
    display_name: Optional[str] = Field(None, min_length=2, max_length=255)
    legal_name: Optional[str] = Field(None, min_length=2, max_length=255)
    business_registration_number: Optional[str] = Field(None, min_length=3, max_length=100)
    
    # Business details
    business_structure: Optional[BusinessStructure] = None
    industry: Optional[Industry] = None
    tax_id: Optional[str] = None
    description: Optional[str] = None
    
    # Contact info
    email: Optional[EmailStr] = None
    phone_country_code: Optional[str] = None
    phone_number: Optional[str] = None
    mobile_country_code: Optional[str] = None
    mobile_number: Optional[str] = None
    fax: Optional[str] = None
    website: Optional[str] = None
    
    # Social media
    facebook: Optional[str] = None
    instagram: Optional[str] = None
    linkedin: Optional[str] = None
    twitter: Optional[str] = None
    
    # Addresses
    mailing_address: Optional[str] = None
    billing_address: Optional[str] = None
    billing_same_as_mailing: Optional[bool] = None
    
    # Invoice settings
    show_email_on_invoice: Optional[bool] = None
    show_phone_on_invoice: Optional[bool] = None
    show_mobile_on_invoice: Optional[bool] = None
    show_fax_on_invoice: Optional[bool] = None
    show_website_on_invoice: Optional[bool] = None
    show_social_media_on_invoice: Optional[bool] = None


# ===== COMPANY RESPONSE SCHEMA =====

class CompanyResponse(BaseModel):
    """Schema for company data in API responses"""
    
    id: int
    display_name: str
    legal_name: str
    slug: str
    business_registration_number: str
    
    # Optional fields
    business_structure: Optional[BusinessStructure] = None
    industry: Optional[Industry] = None
    tax_id: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    
    # Contact
    email: Optional[str] = None
    phone_country_code: Optional[str] = None
    phone_number: Optional[str] = None
    mobile_country_code: Optional[str] = None
    mobile_number: Optional[str] = None
    fax: Optional[str] = None
    website: Optional[str] = None
    
    # Social media
    facebook: Optional[str] = None
    instagram: Optional[str] = None
    linkedin: Optional[str] = None
    twitter: Optional[str] = None
    
    # Addresses
    mailing_address: Optional[str] = None
    billing_address: Optional[str] = None
    billing_same_as_mailing: bool = True
    
    # Invoice settings
    show_email_on_invoice: bool = True
    show_phone_on_invoice: bool = True
    show_mobile_on_invoice: bool = False
    show_fax_on_invoice: bool = False
    show_website_on_invoice: bool = True
    show_social_media_on_invoice: bool = False
    
    # System fields
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ===== USER WITH COMPANY CONTEXT =====

class UserCompanyRole(BaseModel):
    """User's role in a specific company"""
    company_id: int
    company_name: str
    role: str
    is_owner: bool


class CompanyMemberResponse(BaseModel):
    """Company member info"""
    user_id: int
    email: str
    full_name: str
    role: str
    is_owner: bool
    status: str
    joined_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class CompanyListResponse(BaseModel):
    """Schema for returning a list of companies"""
    companies: list[CompanyResponse]

class CompanySelect(BaseModel):
    """Schema for selecting a company"""
    company_id: int

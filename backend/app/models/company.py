# app/models/company.py

"""
Company Model - Complete Business Information
Stores all company/organization details for invoicing and legal compliance.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum


class BusinessStructure(str, enum.Enum):
    """Business structure types (Malaysian focus)"""
    SOLE_PROPRIETORSHIP = "sole_proprietorship"
    PARTNERSHIP = "partnership"
    LLP = "llp"  # Limited Liability Partnership
    PLT = "plt"  # Perkongsian Liabiliti Terhad (Malay)
    SDN_BHD = "sdn_bhd"  # Sendirian Berhad (Private Limited)
    BHD = "bhd"  # Berhad (Public Limited)
    OTHER = "other"


class Industry(str, enum.Enum):
    """Industry types"""
    RETAIL = "retail"
    WHOLESALE = "wholesale"
    MANUFACTURING = "manufacturing"
    SERVICES = "services"
    TECHNOLOGY = "technology"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    HOSPITALITY = "hospitality"
    CONSTRUCTION = "construction"
    AGRICULTURE = "agriculture"
    FINANCE = "finance"
    REAL_ESTATE = "real_estate"
    TRANSPORTATION = "transportation"
    OTHER = "other"


class Company(Base):
    """
    Company table - complete business profile.
    Used for invoicing, legal documents, and multi-company management.
    """
    
    __tablename__ = "companies"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # ===== BASIC INFORMATION (Required at Registration) =====
    
    display_name = Column(
        String(255), 
        nullable=False
    )  # Brand name / Trading name
    
    legal_name = Column(
        String(255), 
        nullable=False
    )  # Official registered business name
    
    slug = Column(
        String(255), 
        unique=True, 
        index=True, 
        nullable=False
    )  # URL-friendly identifier (auto-generated from display_name)
    
    business_registration_number = Column(
        String(100), 
        nullable=False,
        index=True
    )  # SSM number, business license, etc.
    
    # ===== BUSINESS DETAILS (Can update later) =====
    
    business_structure = Column(
        Enum(BusinessStructure),
        nullable=True
    )  # Legal structure
    
    industry = Column(
        Enum(Industry),
        nullable=True
    )  # Business industry/sector
    
    tax_id = Column(String(100))  # Tax identification number (optional)
    
    description = Column(Text)  # Company description
    
    logo_url = Column(String(500))  # Logo file path/URL (optional)
    
    # ===== CONTACT INFORMATION =====
    
    # Email & Phone
    email = Column(String(255))  # Company email
    phone_country_code = Column(String(10))  # e.g., "+60" for Malaysia
    phone_number = Column(String(50))  # Phone without country code
    mobile_country_code = Column(String(10))  # Mobile country code
    mobile_number = Column(String(50))  # Mobile number
    fax = Column(String(50))  # Fax number (optional)
    website = Column(String(255))  # Company website
    
    # Social Media
    facebook = Column(String(255))
    instagram = Column(String(255))
    linkedin = Column(String(255))
    twitter = Column(String(255))
    
    # Addresses
    mailing_address = Column(Text)  # Mailing address
    billing_address = Column(Text)  # Billing address
    billing_same_as_mailing = Column(
        Boolean, 
        default=True
    )  # If True, use mailing address for billing
    
    # ===== INVOICE SETTINGS =====
    
    # What to show on invoices/PDFs
    show_email_on_invoice = Column(Boolean, default=True)
    show_phone_on_invoice = Column(Boolean, default=True)
    show_mobile_on_invoice = Column(Boolean, default=False)
    show_fax_on_invoice = Column(Boolean, default=False)
    show_website_on_invoice = Column(Boolean, default=True)
    show_social_media_on_invoice = Column(Boolean, default=False)
    
    # ===== SYSTEM FIELDS =====
    
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now(), 
        nullable=False
    )
    
    def __repr__(self):
        return f"<Company(id={self.id}, display_name={self.display_name})>"
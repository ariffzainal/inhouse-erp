# app/models/company_member.py

from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from app.database import Base
from app.models.user import UserRole
import enum


class MemberStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"


class CompanyMember(Base):
    __tablename__ = "company_members"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(Enum(UserRole), nullable=False)
    status = Column(Enum(MemberStatus), default=MemberStatus.ACTIVE, nullable=False)
    is_owner = Column(Boolean, default=False, nullable=False)
    joined_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<CompanyMember(user_id={self.user_id}, company_id={self.company_id})>"
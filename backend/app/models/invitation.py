# app/models/invitation.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from app.database import Base
from app.models.user import UserRole
import enum
import secrets


class InvitationStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"


class Invitation(Base):
    __tablename__ = "invitations"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    invited_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    email = Column(String(255), nullable=False, index=True)
    role = Column(Enum(UserRole), nullable=False)
    token = Column(String(255), unique=True, index=True, nullable=False)
    status = Column(Enum(InvitationStatus), default=InvitationStatus.PENDING, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    accepted_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<Invitation(email={self.email}, status={self.status})>"
    
    @staticmethod
    def generate_token():
        return secrets.token_urlsafe(32)
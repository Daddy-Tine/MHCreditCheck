"""
Credit Inquiry model
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class InquiryPurpose(str, enum.Enum):
    """Inquiry purpose enumeration"""
    LOAN_APPLICATION = "LOAN_APPLICATION"
    CREDIT_CARD_APPLICATION = "CREDIT_CARD_APPLICATION"
    EMPLOYMENT = "EMPLOYMENT"
    RENTAL_APPLICATION = "RENTAL_APPLICATION"
    INSURANCE = "INSURANCE"
    ACCOUNT_REVIEW = "ACCOUNT_REVIEW"
    OTHER = "OTHER"


class InquiryStatus(str, enum.Enum):
    """Inquiry status enumeration"""
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    DENIED = "DENIED"
    CANCELLED = "CANCELLED"


class CreditInquiry(Base):
    """Credit inquiry model for tracking credit check requests"""
    __tablename__ = "credit_inquiries"
    
    id = Column(Integer, primary_key=True, index=True)
    consumer_id = Column(Integer, ForeignKey("consumers.id"), nullable=False, index=True)
    bank_id = Column(Integer, ForeignKey("banks.id"), nullable=False, index=True)
    requested_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    purpose = Column(Enum(InquiryPurpose), nullable=False, index=True)
    purpose_description = Column(Text, nullable=True)
    consent_given = Column(Boolean, default=False, nullable=False)
    consent_verified_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(Enum(InquiryStatus), default=InquiryStatus.PENDING, nullable=False, index=True)
    credit_report_id = Column(Integer, ForeignKey("credit_reports.id"), nullable=True)
    ip_address = Column(String(45), nullable=True)  # IPv4 or IPv6
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    consumer = relationship("Consumer", back_populates="credit_inquiries")
    bank = relationship("Bank", back_populates="credit_inquiries")
    
    def __repr__(self):
        return f"<CreditInquiry(id={self.id}, consumer_id={self.consumer_id}, purpose={self.purpose})>"


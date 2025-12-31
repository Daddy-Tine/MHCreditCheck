"""
Bank model
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Bank(Base):
    """Bank/Lender organization model"""
    __tablename__ = "banks"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    license_number = Column(String(100), unique=True, nullable=False, index=True)
    tax_id = Column(String(100), unique=True, nullable=True, index=True)
    contact_email = Column(String(255), nullable=False)
    contact_phone = Column(String(50), nullable=True)
    address = Column(Text, nullable=True)
    api_key = Column(String(255), unique=True, nullable=True, index=True)
    api_key_hash = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_approved = Column(Boolean, default=False, nullable=False)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    approved_by = Column(Integer, nullable=True)  # User ID who approved
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    users = relationship("User", back_populates="bank")
    credit_accounts = relationship("CreditAccount", back_populates="bank")
    credit_inquiries = relationship("CreditInquiry", back_populates="bank")
    
    def __repr__(self):
        return f"<Bank(id={self.id}, name={self.name}, license={self.license_number})>"


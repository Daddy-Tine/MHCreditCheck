"""
Dispute model
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class DisputeStatus(str, enum.Enum):
    """Dispute status enumeration"""
    PENDING = "PENDING"
    UNDER_REVIEW = "UNDER_REVIEW"
    RESOLVED = "RESOLVED"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"


class DisputeReason(str, enum.Enum):
    """Dispute reason enumeration"""
    INCORRECT_BALANCE = "INCORRECT_BALANCE"
    INCORRECT_PAYMENT_HISTORY = "INCORRECT_PAYMENT_HISTORY"
    ACCOUNT_NOT_MINE = "ACCOUNT_NOT_MINE"
    DUPLICATE_ACCOUNT = "DUPLICATE_ACCOUNT"
    FRAUD = "FRAUD"
    IDENTITY_THEFT = "IDENTITY_THEFT"
    OTHER = "OTHER"


class Dispute(Base):
    """Dispute model for consumer credit disputes"""
    __tablename__ = "disputes"
    
    id = Column(Integer, primary_key=True, index=True)
    consumer_id = Column(Integer, ForeignKey("consumers.id"), nullable=False, index=True)
    credit_account_id = Column(Integer, ForeignKey("credit_accounts.id"), nullable=True, index=True)
    reason = Column(Enum(DisputeReason), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(Enum(DisputeStatus), default=DisputeStatus.PENDING, nullable=False, index=True)
    submitted_by = Column(Integer, ForeignKey("users.id"), nullable=True)  # Consumer user
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)  # Admin/Auditor
    resolution_notes = Column(Text, nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    consumer = relationship("Consumer", back_populates="disputes")
    credit_account = relationship("CreditAccount", back_populates="disputes")
    
    def __repr__(self):
        return f"<Dispute(id={self.id}, consumer_id={self.consumer_id}, status={self.status})>"


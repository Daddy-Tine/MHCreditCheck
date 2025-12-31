"""
Consent model
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class ConsentType(str, enum.Enum):
    """Consent type enumeration"""
    CREDIT_REPORT = "CREDIT_REPORT"
    DATA_SHARING = "DATA_SHARING"
    MARKETING = "MARKETING"


class ConsentStatus(str, enum.Enum):
    """Consent status enumeration"""
    GRANTED = "GRANTED"
    REVOKED = "REVOKED"
    EXPIRED = "EXPIRED"


class Consent(Base):
    """Consent model for tracking consumer consent"""
    __tablename__ = "consents"
    
    id = Column(Integer, primary_key=True, index=True)
    consumer_id = Column(Integer, ForeignKey("consumers.id"), nullable=False, index=True)
    consent_type = Column(Enum(ConsentType), nullable=False, index=True)
    status = Column(Enum(ConsentStatus), default=ConsentStatus.GRANTED, nullable=False, index=True)
    bank_id = Column(Integer, ForeignKey("banks.id"), nullable=True, index=True)  # Which bank has consent
    purpose = Column(Text, nullable=True)
    granted_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    revoked_at = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    consumer = relationship("Consumer", back_populates="consents")
    
    def __repr__(self):
        return f"<Consent(id={self.id}, consumer_id={self.consumer_id}, type={self.consent_type}, status={self.status})>"


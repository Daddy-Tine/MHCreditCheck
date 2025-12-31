"""
Consumer model
"""
from sqlalchemy import Column, Integer, String, DateTime, Date, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Consumer(Base):
    """Consumer credit profile model"""
    __tablename__ = "consumers"
    
    id = Column(Integer, primary_key=True, index=True)
    ssn_encrypted = Column(String(512), unique=True, nullable=False, index=True)  # Encrypted SSN
    first_name = Column(String(100), nullable=False, index=True)
    last_name = Column(String(100), nullable=False, index=True)
    middle_name = Column(String(100), nullable=True)
    date_of_birth = Column(Date, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=True, index=True)
    phone = Column(String(50), nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    zip_code = Column(String(20), nullable=True)
    country = Column(String(100), default="Marshall Islands", nullable=False)
    is_frozen = Column(Boolean, default=False, nullable=False)  # Credit freeze flag
    user_id = Column(Integer, nullable=True, unique=True)  # Link to User if registered
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    credit_accounts = relationship("CreditAccount", back_populates="consumer")
    credit_reports = relationship("CreditReport", back_populates="consumer")
    credit_inquiries = relationship("CreditInquiry", back_populates="consumer")
    disputes = relationship("Dispute", back_populates="consumer")
    consents = relationship("Consent", back_populates="consumer")
    
    def __repr__(self):
        return f"<Consumer(id={self.id}, name={self.first_name} {self.last_name})>"


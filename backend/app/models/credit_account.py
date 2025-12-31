"""
Credit Account model
"""
from sqlalchemy import Column, Integer, String, DateTime, Date, Numeric, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class AccountType(str, enum.Enum):
    """Credit account type enumeration"""
    CREDIT_CARD = "CREDIT_CARD"
    MORTGAGE = "MORTGAGE"
    AUTO_LOAN = "AUTO_LOAN"
    PERSONAL_LOAN = "PERSONAL_LOAN"
    STUDENT_LOAN = "STUDENT_LOAN"
    LINE_OF_CREDIT = "LINE_OF_CREDIT"
    OTHER = "OTHER"


class AccountStatus(str, enum.Enum):
    """Account status enumeration"""
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    DELINQUENT = "DELINQUENT"
    CHARGE_OFF = "CHARGE_OFF"
    COLLECTION = "COLLECTION"
    BANKRUPTCY = "BANKRUPTCY"


class PaymentStatus(str, enum.Enum):
    """Payment status enumeration"""
    CURRENT = "CURRENT"
    LATE_30 = "LATE_30"
    LATE_60 = "LATE_60"
    LATE_90 = "LATE_90"
    LATE_120_PLUS = "LATE_120_PLUS"
    NO_PAYMENT = "NO_PAYMENT"


class CreditAccount(Base):
    """Credit account model for tracking individual credit accounts"""
    __tablename__ = "credit_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    consumer_id = Column(Integer, ForeignKey("consumers.id"), nullable=False, index=True)
    bank_id = Column(Integer, ForeignKey("banks.id"), nullable=False, index=True)
    account_number_encrypted = Column(String(512), nullable=False)  # Encrypted account number
    account_type = Column(Enum(AccountType), nullable=False, index=True)
    account_status = Column(Enum(AccountStatus), nullable=False, index=True)
    payment_status = Column(Enum(PaymentStatus), nullable=False, index=True)
    credit_limit = Column(Numeric(15, 2), nullable=True)
    current_balance = Column(Numeric(15, 2), nullable=False, default=0)
    minimum_payment = Column(Numeric(15, 2), nullable=True)
    payment_due_date = Column(Date, nullable=True)
    open_date = Column(Date, nullable=False)
    close_date = Column(Date, nullable=True)
    last_payment_date = Column(Date, nullable=True)
    last_payment_amount = Column(Numeric(15, 2), nullable=True)
    months_since_last_payment = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    is_disputed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    consumer = relationship("Consumer", back_populates="credit_accounts")
    bank = relationship("Bank", back_populates="credit_accounts")
    disputes = relationship("Dispute", back_populates="credit_account")
    
    def __repr__(self):
        return f"<CreditAccount(id={self.id}, type={self.account_type}, status={self.account_status})>"


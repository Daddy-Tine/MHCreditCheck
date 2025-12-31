"""
Credit Account schemas
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from decimal import Decimal
from app.models.credit_account import AccountType, AccountStatus, PaymentStatus


class CreditAccountBase(BaseModel):
    """Base credit account schema"""
    account_type: AccountType
    account_status: AccountStatus
    payment_status: PaymentStatus
    credit_limit: Optional[Decimal] = None
    current_balance: Decimal
    minimum_payment: Optional[Decimal] = None
    payment_due_date: Optional[date] = None
    open_date: date
    close_date: Optional[date] = None
    last_payment_date: Optional[date] = None
    last_payment_amount: Optional[Decimal] = None
    notes: Optional[str] = None


class CreditAccountCreate(CreditAccountBase):
    """Schema for creating a credit account"""
    consumer_id: int
    account_number: str  # Will be encrypted


class CreditAccountUpdate(BaseModel):
    """Schema for updating a credit account"""
    account_status: Optional[AccountStatus] = None
    payment_status: Optional[PaymentStatus] = None
    credit_limit: Optional[Decimal] = None
    current_balance: Optional[Decimal] = None
    minimum_payment: Optional[Decimal] = None
    payment_due_date: Optional[date] = None
    close_date: Optional[date] = None
    last_payment_date: Optional[date] = None
    last_payment_amount: Optional[Decimal] = None
    notes: Optional[str] = None


class CreditAccountResponse(CreditAccountBase):
    """Schema for credit account response"""
    id: int
    consumer_id: int
    bank_id: int
    is_disputed: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}


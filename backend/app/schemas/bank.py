"""
Bank schemas
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class BankBase(BaseModel):
    """Base bank schema"""
    name: str
    license_number: str
    tax_id: Optional[str] = None
    contact_email: EmailStr
    contact_phone: Optional[str] = None
    address: Optional[str] = None


class BankCreate(BankBase):
    """Schema for creating a bank"""
    pass


class BankUpdate(BaseModel):
    """Schema for updating a bank"""
    name: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None


class BankResponse(BankBase):
    """Schema for bank response"""
    id: int
    is_active: bool
    is_approved: bool
    approved_at: Optional[datetime] = None
    approved_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}


class BankApproval(BaseModel):
    """Schema for bank approval"""
    is_approved: bool


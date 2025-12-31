"""
Consumer schemas
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, date


class ConsumerBase(BaseModel):
    """Base consumer schema"""
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    date_of_birth: date
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: str = "Marshall Islands"


class ConsumerCreate(ConsumerBase):
    """Schema for creating a consumer"""
    ssn: str  # Will be encrypted


class ConsumerUpdate(BaseModel):
    """Schema for updating a consumer"""
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    is_frozen: Optional[bool] = None


class ConsumerResponse(ConsumerBase):
    """Schema for consumer response (SSN not included)"""
    id: int
    is_frozen: bool
    user_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}


"""
Credit Report schemas
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class CreditReportBase(BaseModel):
    """Base credit report schema"""
    credit_score: int
    score_factors: Optional[Dict[str, Any]] = None
    report_data: Dict[str, Any]


class CreditReportCreate(BaseModel):
    """Schema for creating a credit report"""
    consumer_id: int


class CreditReportResponse(CreditReportBase):
    """Schema for credit report response"""
    id: int
    consumer_id: int
    version: int
    generated_by: Optional[int] = None
    generated_at: datetime
    expires_at: Optional[datetime] = None
    pdf_path: Optional[str] = None
    created_at: datetime
    
    model_config = {"from_attributes": True}


"""
Credit Inquiries API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.credit_inquiry import CreditInquiry, InquiryPurpose, InquiryStatus
from app.models.consent import Consent, ConsentType, ConsentStatus
from app.models.user import User
from app.schemas.common import APIResponse, PaginatedResponse
from app.api.dependencies import get_current_active_user
from datetime import datetime

router = APIRouter()


@router.post("/", response_model=APIResponse[dict], status_code=status.HTTP_201_CREATED)
async def create_inquiry(
    consumer_id: int,
    purpose: InquiryPurpose,
    purpose_description: str = None,
    request: Request = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a credit inquiry"""
    # Verify consent
    consent = db.query(Consent).filter(
        Consent.consumer_id == consumer_id,
        Consent.consent_type == ConsentType.CREDIT_REPORT,
        Consent.status == ConsentStatus.GRANTED,
        Consent.bank_id == current_user.bank_id
    ).first()
    
    if not consent:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Consumer consent required for credit inquiry"
        )
    
    # Get IP address and user agent
    ip_address = request.client.host if request else None
    user_agent = request.headers.get("user-agent") if request else None
    
    # Create inquiry
    db_inquiry = CreditInquiry(
        consumer_id=consumer_id,
        bank_id=current_user.bank_id,
        requested_by=current_user.id,
        purpose=purpose,
        purpose_description=purpose_description,
        consent_given=True,
        consent_verified_at=datetime.utcnow(),
        status=InquiryStatus.APPROVED,
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    db.add(db_inquiry)
    db.commit()
    db.refresh(db_inquiry)
    
    return APIResponse(
        success=True,
        data={"inquiry_id": db_inquiry.id, "status": db_inquiry.status.value},
        meta={"message": "Credit inquiry created successfully"}
    )


@router.get("/", response_model=PaginatedResponse[dict])
async def get_inquiries(
    skip: int = 0,
    limit: int = 100,
    consumer_id: int = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get credit inquiries"""
    query = db.query(CreditInquiry)
    
    # Filter by consumer if provided
    if consumer_id:
        query = query.filter(CreditInquiry.consumer_id == consumer_id)
    
    # Filter by bank if user is not admin
    if current_user.role.value != "ADMIN" and current_user.bank_id:
        query = query.filter(CreditInquiry.bank_id == current_user.bank_id)
    
    inquiries = query.order_by(CreditInquiry.created_at.desc()).offset(skip).limit(limit).all()
    total = query.count()
    
    inquiry_data = [
        {
            "id": inv.id,
            "consumer_id": inv.consumer_id,
            "bank_id": inv.bank_id,
            "purpose": inv.purpose.value,
            "status": inv.status.value,
            "created_at": inv.created_at.isoformat()
        }
        for inv in inquiries
    ]
    
    return PaginatedResponse(
        success=True,
        data=inquiry_data,
        meta={
            "page": skip // limit + 1,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit
        }
    )


"""
Credit Reports API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.credit_report import CreditReport
from app.models.consumer import Consumer
from app.models.credit_account import CreditAccount
from app.models.consent import Consent, ConsentType, ConsentStatus
from app.models.user import User
from app.schemas.credit_report import CreditReportCreate, CreditReportResponse
from app.schemas.common import APIResponse
from app.api.dependencies import get_current_active_user, require_permission_dependency
from app.utils.permissions import Permission, can_access_consumer_data
from app.utils.credit_scoring import calculate_credit_score
from datetime import datetime, timedelta

router = APIRouter()


@router.post("/", response_model=APIResponse[CreditReportResponse], status_code=status.HTTP_201_CREATED)
async def generate_credit_report(
    report_data: CreditReportCreate,
    current_user: User = Depends(require_permission_dependency(Permission.GENERATE_CREDIT_REPORT)),
    db: Session = Depends(get_db)
):
    """Generate a credit report for a consumer"""
    # Check if consumer exists
    consumer = db.query(Consumer).filter(Consumer.id == report_data.consumer_id).first()
    if not consumer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consumer not found"
        )
    
    # Check if credit is frozen
    if consumer.is_frozen:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Consumer credit is frozen"
        )
    
    # Verify consent (unless user is admin or consumer viewing own report)
    if current_user.role.value != "ADMIN" and current_user.role.value != "CONSUMER":
        consent = db.query(Consent).filter(
            Consent.consumer_id == report_data.consumer_id,
            Consent.consent_type == ConsentType.CREDIT_REPORT,
            Consent.status == ConsentStatus.GRANTED,
            Consent.bank_id == current_user.bank_id
        ).first()
        
        if not consent:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Consumer consent required to generate credit report"
            )
    
    # Get all credit accounts for consumer
    credit_accounts = db.query(CreditAccount).filter(
        CreditAccount.consumer_id == report_data.consumer_id
    ).all()
    
    # Calculate credit score
    score_result = calculate_credit_score(consumer, credit_accounts)
    
    # Prepare report data
    report_json = {
        "consumer": {
            "id": consumer.id,
            "name": f"{consumer.first_name} {consumer.last_name}",
            "date_of_birth": consumer.date_of_birth.isoformat()
        },
        "credit_score": score_result["score"],
        "score_factors": score_result.get("factors", {}),
        "accounts": [
            {
                "id": acc.id,
                "type": acc.account_type.value,
                "status": acc.account_status.value,
                "payment_status": acc.payment_status.value,
                "balance": float(acc.current_balance),
                "credit_limit": float(acc.credit_limit) if acc.credit_limit else None,
                "open_date": acc.open_date.isoformat()
            }
            for acc in credit_accounts
        ],
        "generated_at": datetime.utcnow().isoformat()
    }
    
    # Create credit report
    db_report = CreditReport(
        consumer_id=report_data.consumer_id,
        credit_score=score_result["score"],
        score_factors=score_result.get("factors", {}),
        report_data=report_json,
        generated_by=current_user.id,
        expires_at=datetime.utcnow() + timedelta(days=30)  # Reports expire in 30 days
    )
    
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    
    return APIResponse(
        success=True,
        data=CreditReportResponse.model_validate(db_report),
        meta={"message": "Credit report generated successfully"}
    )


@router.get("/{report_id}", response_model=APIResponse[CreditReportResponse])
async def get_credit_report(
    report_id: int,
    current_user: User = Depends(require_permission_dependency(Permission.VIEW_CREDIT_REPORT)),
    db: Session = Depends(get_db)
):
    """Get credit report by ID"""
    report = db.query(CreditReport).filter(CreditReport.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Credit report not found"
        )
    
    # Verify access
    if not can_access_consumer_data(current_user, report.consumer_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this credit report"
        )
    
    return APIResponse(success=True, data=CreditReportResponse.model_validate(report))


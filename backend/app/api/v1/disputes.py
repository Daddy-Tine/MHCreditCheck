"""
Disputes API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.dispute import Dispute, DisputeStatus, DisputeReason
from app.models.user import User
from app.schemas.common import APIResponse, PaginatedResponse
from app.api.dependencies import get_current_active_user, require_permission_dependency
from app.utils.permissions import Permission
from datetime import datetime

router = APIRouter()


@router.post("/", response_model=APIResponse[dict], status_code=status.HTTP_201_CREATED)
async def create_dispute(
    consumer_id: int,
    credit_account_id: int = None,
    reason: DisputeReason = None,
    description: str = None,
    current_user: User = Depends(require_permission_dependency(Permission.CREATE_DISPUTE)),
    db: Session = Depends(get_db)
):
    """Create a dispute"""
    db_dispute = Dispute(
        consumer_id=consumer_id,
        credit_account_id=credit_account_id,
        reason=reason,
        description=description,
        status=DisputeStatus.PENDING,
        submitted_by=current_user.id
    )
    
    db.add(db_dispute)
    db.commit()
    db.refresh(db_dispute)
    
    return APIResponse(
        success=True,
        data={"dispute_id": db_dispute.id, "status": db_dispute.status.value},
        meta={"message": "Dispute created successfully"}
    )


@router.get("/", response_model=PaginatedResponse[dict])
async def get_disputes(
    skip: int = 0,
    limit: int = 100,
    status_filter: DisputeStatus = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get disputes"""
    query = db.query(Dispute)
    
    # Filter by status if provided
    if status_filter:
        query = query.filter(Dispute.status == status_filter)
    
    # Consumers can only see their own disputes
    if current_user.role.value == "CONSUMER":
        query = query.filter(Dispute.consumer_id == current_user.id)
    
    disputes = query.order_by(Dispute.created_at.desc()).offset(skip).limit(limit).all()
    total = query.count()
    
    dispute_data = [
        {
            "id": d.id,
            "consumer_id": d.consumer_id,
            "reason": d.reason.value,
            "status": d.status.value,
            "created_at": d.created_at.isoformat()
        }
        for d in disputes
    ]
    
    return PaginatedResponse(
        success=True,
        data=dispute_data,
        meta={
            "page": skip // limit + 1,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit
        }
    )


@router.post("/{dispute_id}/resolve", response_model=APIResponse[dict])
async def resolve_dispute(
    dispute_id: int,
    resolution_notes: str,
    status: DisputeStatus,
    current_user: User = Depends(require_permission_dependency(Permission.RESOLVE_DISPUTE)),
    db: Session = Depends(get_db)
):
    """Resolve a dispute (admin/auditor only)"""
    dispute = db.query(Dispute).filter(Dispute.id == dispute_id).first()
    if not dispute:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispute not found"
        )
    
    dispute.status = status
    dispute.resolution_notes = resolution_notes
    dispute.reviewed_by = current_user.id
    dispute.resolved_at = datetime.utcnow()
    
    db.commit()
    
    return APIResponse(
        success=True,
        data={"dispute_id": dispute.id, "status": dispute.status.value},
        meta={"message": "Dispute resolved successfully"}
    )


"""
Audit Logs API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.audit_log import AuditLog
from app.models.user import User
from app.schemas.common import PaginatedResponse
from app.api.dependencies import require_permission_dependency
from app.utils.permissions import Permission

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[dict])
async def get_audit_logs(
    skip: int = 0,
    limit: int = 100,
    user_id: int = None,
    resource_type: str = None,
    current_user: User = Depends(require_permission_dependency(Permission.VIEW_AUDIT_LOGS)),
    db: Session = Depends(get_db)
):
    """Get audit logs (admin/auditor only)"""
    query = db.query(AuditLog)
    
    # Filter by user if provided
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)
    
    # Filter by resource type if provided
    if resource_type:
        query = query.filter(AuditLog.resource_type == resource_type)
    
    logs = query.order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()
    total = query.count()
    
    log_data = [
        {
            "id": log.id,
            "user_id": log.user_id,
            "action": log.action.value,
            "resource_type": log.resource_type,
            "resource_id": log.resource_id,
            "ip_address": log.ip_address,
            "created_at": log.created_at.isoformat()
        }
        for log in logs
    ]
    
    return PaginatedResponse(
        success=True,
        data=log_data,
        meta={
            "page": skip // limit + 1,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit
        }
    )


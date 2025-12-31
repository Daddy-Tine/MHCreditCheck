"""
Banks API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.bank import Bank
from app.models.user import User, UserRole
from app.schemas.bank import BankCreate, BankUpdate, BankResponse, BankApproval
from app.schemas.common import APIResponse, PaginatedResponse
from app.api.dependencies import get_current_active_user, require_permission_dependency
from app.utils.permissions import Permission
from app.utils.security import generate_api_key, get_password_hash
from datetime import datetime

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[BankResponse])
async def get_banks(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_permission_dependency(Permission.VIEW_BANK)),
    db: Session = Depends(get_db)
):
    """Get list of banks"""
    banks = db.query(Bank).offset(skip).limit(limit).all()
    total = db.query(Bank).count()
    
    return PaginatedResponse(
        success=True,
        data=[BankResponse.model_validate(bank) for bank in banks],
        meta={
            "page": skip // limit + 1,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit
        }
    )


@router.get("/{bank_id}", response_model=APIResponse[BankResponse])
async def get_bank(
    bank_id: int,
    current_user: User = Depends(require_permission_dependency(Permission.VIEW_BANK)),
    db: Session = Depends(get_db)
):
    """Get bank by ID"""
    bank = db.query(Bank).filter(Bank.id == bank_id).first()
    if not bank:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bank not found"
        )
    return APIResponse(success=True, data=BankResponse.from_orm(bank))


@router.post("/", response_model=APIResponse[BankResponse], status_code=status.HTTP_201_CREATED)
async def create_bank(
    bank_data: BankCreate,
    current_user: User = Depends(require_permission_dependency(Permission.CREATE_BANK)),
    db: Session = Depends(get_db)
):
    """Create a new bank (admin only)"""
    existing_bank = db.query(Bank).filter(Bank.license_number == bank_data.license_number).first()
    if existing_bank:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bank with this license number already exists"
        )
    
    # Generate API key
    api_key = generate_api_key()
    api_key_hash = get_password_hash(api_key)
    
    db_bank = Bank(
        name=bank_data.name,
        license_number=bank_data.license_number,
        tax_id=bank_data.tax_id,
        contact_email=bank_data.contact_email,
        contact_phone=bank_data.contact_phone,
        address=bank_data.address,
        api_key_hash=api_key_hash,
        is_active=True,
        is_approved=False
    )
    
    db.add(db_bank)
    db.commit()
    db.refresh(db_bank)
    
    # Return API key in response (only shown once)
    response_data = BankResponse.from_orm(db_bank)
    response_data.api_key = api_key  # This won't be in the model, but we'll add it
    
    return APIResponse(
        success=True,
        data=BankResponse.model_validate(db_bank),
        meta={"api_key": api_key, "message": "Bank created. Save the API key securely."}
    )


@router.put("/{bank_id}", response_model=APIResponse[BankResponse])
async def update_bank(
    bank_id: int,
    bank_data: BankUpdate,
    current_user: User = Depends(require_permission_dependency(Permission.UPDATE_BANK)),
    db: Session = Depends(get_db)
):
    """Update bank"""
    bank = db.query(Bank).filter(Bank.id == bank_id).first()
    if not bank:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bank not found"
        )
    
    update_data = bank_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(bank, field, value)
    
    db.commit()
    db.refresh(bank)
    
    return APIResponse(
        success=True,
        data=BankResponse.from_orm(bank),
        meta={"message": "Bank updated successfully"}
    )


@router.post("/{bank_id}/approve", response_model=APIResponse[BankResponse])
async def approve_bank(
    bank_id: int,
    approval: BankApproval,
    current_user: User = Depends(require_permission_dependency(Permission.APPROVE_BANK)),
    db: Session = Depends(get_db)
):
    """Approve or reject a bank (admin only)"""
    bank = db.query(Bank).filter(Bank.id == bank_id).first()
    if not bank:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bank not found"
        )
    
    bank.is_approved = approval.is_approved
    if approval.is_approved:
        bank.approved_at = datetime.utcnow()
        bank.approved_by = current_user.id
    
    db.commit()
    db.refresh(bank)
    
    return APIResponse(
        success=True,
        data=BankResponse.from_orm(bank),
        meta={"message": f"Bank {'approved' if approval.is_approved else 'rejected'} successfully"}
    )


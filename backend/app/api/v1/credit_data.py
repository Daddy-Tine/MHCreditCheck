"""
Credit Data API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.credit_account import CreditAccount
from app.models.user import User
from app.schemas.credit_account import CreditAccountCreate, CreditAccountUpdate, CreditAccountResponse
from app.schemas.common import APIResponse, PaginatedResponse
from app.api.dependencies import get_current_active_user, require_permission_dependency
from app.utils.permissions import Permission, can_access_bank_data
from app.utils.security import encrypt_sensitive_data

router = APIRouter()


@router.post("/", response_model=APIResponse[CreditAccountResponse], status_code=status.HTTP_201_CREATED)
async def submit_credit_data(
    credit_data: CreditAccountCreate,
    current_user: User = Depends(require_permission_dependency(Permission.SUBMIT_CREDIT_DATA)),
    db: Session = Depends(get_db)
):
    """Submit credit account data"""
    # Verify user can submit data for their bank
    if current_user.bank_id and not can_access_bank_data(current_user, current_user.bank_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot submit data for this bank"
        )
    
    # Encrypt account number
    encrypted_account_number = encrypt_sensitive_data(credit_data.account_number)
    
    db_account = CreditAccount(
        consumer_id=credit_data.consumer_id,
        bank_id=current_user.bank_id or 1,  # Use user's bank or default
        account_number_encrypted=encrypted_account_number,
        account_type=credit_data.account_type,
        account_status=credit_data.account_status,
        payment_status=credit_data.payment_status,
        credit_limit=credit_data.credit_limit,
        current_balance=credit_data.current_balance,
        minimum_payment=credit_data.minimum_payment,
        payment_due_date=credit_data.payment_due_date,
        open_date=credit_data.open_date,
        close_date=credit_data.close_date,
        last_payment_date=credit_data.last_payment_date,
        last_payment_amount=credit_data.last_payment_amount,
        notes=credit_data.notes
    )
    
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    
    return APIResponse(
        success=True,
        data=CreditAccountResponse.model_validate(db_account),
        meta={"message": "Credit data submitted successfully"}
    )


@router.get("/", response_model=PaginatedResponse[CreditAccountResponse])
async def get_credit_data(
    skip: int = 0,
    limit: int = 100,
    consumer_id: int = None,
    current_user: User = Depends(require_permission_dependency(Permission.VIEW_CREDIT_REPORT)),
    db: Session = Depends(get_db)
):
    """Get credit account data"""
    query = db.query(CreditAccount)
    
    # Filter by consumer if provided
    if consumer_id:
        query = query.filter(CreditAccount.consumer_id == consumer_id)
    
    # Filter by bank if user is not admin
    if current_user.role.value != "ADMIN" and current_user.bank_id:
        query = query.filter(CreditAccount.bank_id == current_user.bank_id)
    
    accounts = query.offset(skip).limit(limit).all()
    total = query.count()
    
    return PaginatedResponse(
        success=True,
        data=[CreditAccountResponse.model_validate(account) for account in accounts],
        meta={
            "page": skip // limit + 1,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit
        }
    )


@router.put("/{account_id}", response_model=APIResponse[CreditAccountResponse])
async def update_credit_data(
    account_id: int,
    credit_data: CreditAccountUpdate,
    current_user: User = Depends(require_permission_dependency(Permission.UPDATE_CREDIT_DATA)),
    db: Session = Depends(get_db)
):
    """Update credit account data"""
    account = db.query(CreditAccount).filter(CreditAccount.id == account_id).first()
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Credit account not found"
        )
    
    # Verify access
    if not can_access_bank_data(current_user, account.bank_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update data for this bank"
        )
    
    update_data = credit_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(account, field, value)
    
    db.commit()
    db.refresh(account)
    
    return APIResponse(
        success=True,
        data=CreditAccountResponse.from_orm(account),
        meta={"message": "Credit data updated successfully"}
    )


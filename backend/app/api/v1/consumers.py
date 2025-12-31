"""
Consumers API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.consumer import Consumer
from app.models.user import User
from app.schemas.consumer import ConsumerCreate, ConsumerUpdate, ConsumerResponse
from app.schemas.common import APIResponse, PaginatedResponse
from app.api.dependencies import get_current_active_user
from app.utils.security import encrypt_sensitive_data

router = APIRouter()


@router.post("/", response_model=APIResponse[ConsumerResponse], status_code=status.HTTP_201_CREATED)
async def create_consumer(
    consumer_data: ConsumerCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a consumer profile"""
    # Encrypt SSN
    encrypted_ssn = encrypt_sensitive_data(consumer_data.ssn)
    
    # Check if consumer already exists (by SSN)
    existing = db.query(Consumer).filter(Consumer.ssn_encrypted == encrypted_ssn).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Consumer with this SSN already exists"
        )
    
    db_consumer = Consumer(
        ssn_encrypted=encrypted_ssn,
        first_name=consumer_data.first_name,
        last_name=consumer_data.last_name,
        middle_name=consumer_data.middle_name,
        date_of_birth=consumer_data.date_of_birth,
        email=consumer_data.email,
        phone=consumer_data.phone,
        address=consumer_data.address,
        city=consumer_data.city,
        state=consumer_data.state,
        zip_code=consumer_data.zip_code,
        country=consumer_data.country
    )
    
    db.add(db_consumer)
    db.commit()
    db.refresh(db_consumer)
    
    return APIResponse(
        success=True,
        data=ConsumerResponse.model_validate(db_consumer),
        meta={"message": "Consumer created successfully"}
    )


@router.get("/{consumer_id}", response_model=APIResponse[ConsumerResponse])
async def get_consumer(
    consumer_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get consumer by ID"""
    consumer = db.query(Consumer).filter(Consumer.id == consumer_id).first()
    if not consumer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consumer not found"
        )
    
    # Consumers can only view their own data
    if current_user.role.value == "CONSUMER" and consumer.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return APIResponse(success=True, data=ConsumerResponse.from_orm(consumer))


@router.put("/{consumer_id}/freeze", response_model=APIResponse[ConsumerResponse])
async def freeze_credit(
    consumer_id: int,
    is_frozen: bool,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Freeze or unfreeze consumer credit"""
    consumer = db.query(Consumer).filter(Consumer.id == consumer_id).first()
    if not consumer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consumer not found"
        )
    
    # Only consumer or admin can freeze
    if current_user.role.value == "CONSUMER" and consumer.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    consumer.is_frozen = is_frozen
    db.commit()
    db.refresh(consumer)
    
    return APIResponse(
        success=True,
        data=ConsumerResponse.model_validate(consumer),
        meta={"message": f"Credit {'frozen' if is_frozen else 'unfrozen'} successfully"}
    )


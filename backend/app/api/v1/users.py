"""
Users API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.schemas.common import APIResponse, PaginatedResponse
from app.api.dependencies import get_current_active_user, require_permission_dependency
from app.utils.permissions import Permission
from app.utils.security import get_password_hash

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_permission_dependency(Permission.VIEW_USER)),
    db: Session = Depends(get_db)
):
    """Get list of users (admin only)"""
    users = db.query(User).offset(skip).limit(limit).all()
    total = db.query(User).count()
    
    return PaginatedResponse(
        success=True,
        data=[UserResponse.model_validate(user) for user in users],
        meta={
            "page": skip // limit + 1,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit
        }
    )


@router.get("/{user_id}", response_model=APIResponse[UserResponse])
async def get_user(
    user_id: int,
    current_user: User = Depends(require_permission_dependency(Permission.VIEW_USER)),
    db: Session = Depends(get_db)
):
    """Get user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return APIResponse(success=True, data=UserResponse.from_orm(user))


@router.post("/", response_model=APIResponse[UserResponse], status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    current_user: User = Depends(require_permission_dependency(Permission.CREATE_USER)),
    db: Session = Depends(get_db)
):
    """Create a new user (admin only)"""
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        password_hash=hashed_password,
        full_name=user_data.full_name,
        role=user_data.role,
        bank_id=user_data.bank_id,
        is_active=True,
        is_verified=True
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return APIResponse(
        success=True,
        data=UserResponse.model_validate(db_user),
        meta={"message": "User created successfully"}
    )


@router.put("/{user_id}", response_model=APIResponse[UserResponse])
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(require_permission_dependency(Permission.UPDATE_USER)),
    db: Session = Depends(get_db)
):
    """Update user (admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    update_data = user_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    return APIResponse(
        success=True,
        data=UserResponse.model_validate(user),
        meta={"message": "User updated successfully"}
    )


@router.delete("/{user_id}", response_model=APIResponse[dict])
async def delete_user(
    user_id: int,
    current_user: User = Depends(require_permission_dependency(Permission.DELETE_USER)),
    db: Session = Depends(get_db)
):
    """Delete user (admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db.delete(user)
    db.commit()
    
    return APIResponse(
        success=True,
        data={"message": "User deleted successfully"}
    )


"""
Common schemas for API responses
"""
from pydantic import BaseModel
from typing import Optional, Any, Dict, Generic, TypeVar

T = TypeVar('T')


class APIResponse(BaseModel, Generic[T]):
    """Standard API response format"""
    success: bool
    data: Optional[T] = None
    error: Optional[Dict[str, Any]] = None
    meta: Optional[Dict[str, Any]] = None


class PaginationMeta(BaseModel):
    """Pagination metadata"""
    page: int
    limit: int
    total: int
    pages: int


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response format"""
    success: bool = True
    data: list[T]
    meta: PaginationMeta
    error: Optional[Dict[str, Any]] = None


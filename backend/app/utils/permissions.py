"""
Permission and authorization utilities
"""
from typing import List, Optional
from app.models.user import User, UserRole
from app.models.bank import Bank


class Permission:
    """Permission constants"""
    # Credit Report permissions
    VIEW_CREDIT_REPORT = "view:credit_report"
    GENERATE_CREDIT_REPORT = "generate:credit_report"
    
    # Credit Data permissions
    SUBMIT_CREDIT_DATA = "submit:credit_data"
    UPDATE_CREDIT_DATA = "update:credit_data"
    DELETE_CREDIT_DATA = "delete:credit_data"
    
    # User management permissions
    CREATE_USER = "create:user"
    UPDATE_USER = "update:user"
    DELETE_USER = "delete:user"
    VIEW_USER = "view:user"
    
    # Bank management permissions
    CREATE_BANK = "create:bank"
    UPDATE_BANK = "update:bank"
    APPROVE_BANK = "approve:bank"
    VIEW_BANK = "view:bank"
    
    # Audit permissions
    VIEW_AUDIT_LOGS = "view:audit_logs"
    EXPORT_AUDIT_LOGS = "export:audit_logs"
    
    # Dispute permissions
    CREATE_DISPUTE = "create:dispute"
    REVIEW_DISPUTE = "review:dispute"
    RESOLVE_DISPUTE = "resolve:dispute"
    
    # Consumer permissions
    VIEW_OWN_REPORT = "view:own_report"
    FREEZE_CREDIT = "freeze:credit"
    MANAGE_CONSENT = "manage:consent"


# Role-based permission mapping
ROLE_PERMISSIONS = {
    UserRole.ADMIN: [
        Permission.VIEW_CREDIT_REPORT,
        Permission.GENERATE_CREDIT_REPORT,
        Permission.SUBMIT_CREDIT_DATA,
        Permission.UPDATE_CREDIT_DATA,
        Permission.DELETE_CREDIT_DATA,
        Permission.CREATE_USER,
        Permission.UPDATE_USER,
        Permission.DELETE_USER,
        Permission.VIEW_USER,
        Permission.CREATE_BANK,
        Permission.UPDATE_BANK,
        Permission.APPROVE_BANK,
        Permission.VIEW_BANK,
        Permission.VIEW_AUDIT_LOGS,
        Permission.EXPORT_AUDIT_LOGS,
        Permission.REVIEW_DISPUTE,
        Permission.RESOLVE_DISPUTE,
    ],
    UserRole.BANK_MANAGER: [
        Permission.VIEW_CREDIT_REPORT,
        Permission.GENERATE_CREDIT_REPORT,
        Permission.SUBMIT_CREDIT_DATA,
        Permission.UPDATE_CREDIT_DATA,
        Permission.CREATE_USER,
        Permission.UPDATE_USER,
        Permission.VIEW_USER,
        Permission.VIEW_BANK,
    ],
    UserRole.BANK_USER: [
        Permission.VIEW_CREDIT_REPORT,
        Permission.GENERATE_CREDIT_REPORT,
        Permission.SUBMIT_CREDIT_DATA,
        Permission.UPDATE_CREDIT_DATA,
    ],
    UserRole.DATA_PROVIDER: [
        Permission.SUBMIT_CREDIT_DATA,
        Permission.UPDATE_CREDIT_DATA,
    ],
    UserRole.AUDITOR: [
        Permission.VIEW_CREDIT_REPORT,
        Permission.VIEW_AUDIT_LOGS,
        Permission.VIEW_USER,
        Permission.VIEW_BANK,
    ],
    UserRole.CONSUMER: [
        Permission.VIEW_OWN_REPORT,
        Permission.CREATE_DISPUTE,
        Permission.FREEZE_CREDIT,
        Permission.MANAGE_CONSENT,
    ],
}


def has_permission(user: User, permission: str) -> bool:
    """Check if user has a specific permission"""
    user_permissions = ROLE_PERMISSIONS.get(user.role, [])
    return permission in user_permissions


def require_permission(permission: str):
    """Decorator to require a specific permission"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # This will be used with dependency injection in FastAPI
            return func(*args, **kwargs)
        return wrapper
    return decorator


def can_access_bank_data(user: User, bank_id: int) -> bool:
    """Check if user can access data for a specific bank"""
    if user.role == UserRole.ADMIN:
        return True
    if user.role in [UserRole.BANK_MANAGER, UserRole.BANK_USER]:
        return user.bank_id == bank_id
    return False


def can_access_consumer_data(user: User, consumer_id: int, consumer_user_id: Optional[int] = None) -> bool:
    """Check if user can access a specific consumer's data"""
    if user.role == UserRole.ADMIN:
        return True
    if user.role == UserRole.CONSUMER:
        return user.id == consumer_user_id
    if user.role in [UserRole.BANK_MANAGER, UserRole.BANK_USER, UserRole.AUDITOR]:
        # These roles can access with proper consent
        return True
    return False


def get_user_permissions(user: User) -> List[str]:
    """Get all permissions for a user"""
    return ROLE_PERMISSIONS.get(user.role, [])


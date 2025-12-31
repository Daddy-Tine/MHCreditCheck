"""
Audit logging middleware
"""
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.audit_log import AuditLog, AuditAction
from app.utils.security import verify_token
from app.utils.security import mask_sensitive_data
import json
import time


class AuditMiddleware(BaseHTTPMiddleware):
    """Middleware to automatically log API requests to audit log"""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Skip audit logging for health checks and docs
        if request.url.path in ["/health", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)
        
        # Get user from token if available
        user_id = None
        token = request.headers.get("authorization", "").replace("Bearer ", "")
        if token:
            payload = verify_token(token, "access")
            if payload:
                user_id = payload.get("sub")
        
        # Read request body if available
        request_body = None
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.body()
                if body:
                    # Try to parse as JSON
                    try:
                        request_body = json.loads(body.decode())
                        # Mask sensitive fields
                        request_body = self._mask_sensitive_data(request_body)
                    except:
                        request_body = {"raw": mask_sensitive_data(body.decode()[:500])}
            except:
                pass
        
        # Process request
        response = await call_next(request)
        
        # Calculate response time
        process_time = time.time() - start_time
        
        # Determine audit action based on HTTP method
        action_map = {
            "GET": AuditAction.READ,
            "POST": AuditAction.CREATE,
            "PUT": AuditAction.UPDATE,
            "PATCH": AuditAction.UPDATE,
            "DELETE": AuditAction.DELETE,
        }
        action = action_map.get(request.method, AuditAction.READ)
        
        # Log to database (async in background would be better, but this works)
        try:
            db: Session = SessionLocal()
            audit_log = AuditLog(
                user_id=user_id,
                action=action,
                resource_type=request.url.path.split("/")[-1] if request.url.path else "unknown",
                ip_address=request.client.host if request.client else None,
                user_agent=request.headers.get("user-agent"),
                request_method=request.method,
                request_path=str(request.url.path),
                request_body=request_body,
                response_status=response.status_code,
                metadata={
                    "process_time": process_time,
                    "query_params": dict(request.query_params) if request.query_params else None
                }
            )
            db.add(audit_log)
            db.commit()
            db.close()
        except Exception as e:
            # Don't fail the request if audit logging fails
            print(f"Audit logging error: {e}")
        
        return response
    
    def _mask_sensitive_data(self, data: dict) -> dict:
        """Recursively mask sensitive data in request body"""
        sensitive_fields = ["password", "ssn", "account_number", "api_key", "secret"]
        if isinstance(data, dict):
            return {
                k: mask_sensitive_data(str(v)) if k.lower() in sensitive_fields else self._mask_sensitive_data(v)
                for k, v in data.items()
            }
        elif isinstance(data, list):
            return [self._mask_sensitive_data(item) for item in data]
        return data


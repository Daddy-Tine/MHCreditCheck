"""
Rate limiting middleware
"""
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from app.config import settings
from datetime import datetime, timedelta
from typing import Dict
import time

# In-memory rate limit store (use Redis if available)
_rate_limit_store: Dict[str, Dict[str, any]] = {}


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware to rate limit API requests"""
    
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for health checks and docs
        if request.url.path in ["/health", "/docs", "/redoc", "/openapi.json", "/"]:
            return await call_next(request)
        
        # Get client identifier
        client_id = self._get_client_id(request)
        
        # Check rate limits
        if not self._check_rate_limit(client_id, request.url.path):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please try again later.",
                headers={"Retry-After": "60"}
            )
        
        response = await call_next(request)
        
        # Add rate limit headers
        remaining = self._get_remaining_requests(client_id)
        response.headers["X-RateLimit-Limit"] = str(settings.RATE_LIMIT_PER_MINUTE)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        
        return response
    
    def _get_client_id(self, request: Request) -> str:
        """Get client identifier (IP address or user ID)"""
        # Try to get user ID from token if available
        # For now, use IP address
        return request.client.host if request.client else "unknown"
    
    def _check_rate_limit(self, client_id: str, path: str) -> bool:
        """Check if request is within rate limit"""
        now = datetime.utcnow()
        minute_key = f"{client_id}:{path}:minute"
        hour_key = f"{client_id}:{path}:hour"
        
        # Clean old entries (simple cleanup)
        if len(_rate_limit_store) > 10000:
            _rate_limit_store.clear()
        
        # Check per-minute limit
        if minute_key not in _rate_limit_store:
            _rate_limit_store[minute_key] = {
                "count": 0,
                "reset_time": now + timedelta(minutes=1)
            }
        
        minute_data = _rate_limit_store[minute_key]
        
        # Reset if time expired
        if now > minute_data["reset_time"]:
            minute_data["count"] = 0
            minute_data["reset_time"] = now + timedelta(minutes=1)
        
        # Check limit
        if minute_data["count"] >= settings.RATE_LIMIT_PER_MINUTE:
            return False
        
        # Increment count
        minute_data["count"] += 1
        
        # Check per-hour limit (similar logic)
        if hour_key not in _rate_limit_store:
            _rate_limit_store[hour_key] = {
                "count": 0,
                "reset_time": now + timedelta(hours=1)
            }
        
        hour_data = _rate_limit_store[hour_key]
        
        if now > hour_data["reset_time"]:
            hour_data["count"] = 0
            hour_data["reset_time"] = now + timedelta(hours=1)
        
        if hour_data["count"] >= settings.RATE_LIMIT_PER_HOUR:
            return False
        
        hour_data["count"] += 1
        
        return True
    
    def _get_remaining_requests(self, client_id: str) -> int:
        """Get remaining requests for client"""
        minute_key = f"{client_id}:minute"
        if minute_key in _rate_limit_store:
            data = _rate_limit_store[minute_key]
            return max(0, settings.RATE_LIMIT_PER_MINUTE - data["count"])
        return settings.RATE_LIMIT_PER_MINUTE


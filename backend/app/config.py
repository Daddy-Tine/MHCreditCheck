"""
Application configuration management
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = "Credit Check API"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    
    # Database
    DATABASE_URL: str
    POSTGRES_USER: str = "creditcheck"
    POSTGRES_PASSWORD: str = "changeme"
    POSTGRES_DB: str = "creditcheck"
    
    # Redis (Optional - for caching and rate limiting)
    REDIS_URL: str = ""  # Leave empty to disable Redis
    USE_REDIS: bool = False  # Set to True to enable Redis
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Email (Resend)
    RESEND_API_KEY: str = ""  # Get from https://resend.com/api-keys
    EMAIL_FROM: str = "noreply@creditcheck.mh"  # Must be verified in Resend
    
    # Legacy SMTP (optional fallback)
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    USE_SMTP: bool = False  # Set to True to use SMTP instead of Resend
    
    # Encryption
    ENCRYPTION_KEY: str
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    # File Storage
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    
    # Sentry (Error Tracking - Optional)
    SENTRY_DSN: str = ""  # Get from https://sentry.io
    ENABLE_SENTRY: bool = False  # Set to True to enable Sentry
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Parse CORS_ORIGINS from comma-separated string if needed
def get_cors_origins() -> List[str]:
    """Get CORS origins from environment"""
    cors_env = os.getenv("CORS_ORIGINS", "")
    if cors_env:
        return [origin.strip() for origin in cors_env.split(",")]
    return ["http://localhost:3000", "http://localhost:5173"]


settings = Settings()
settings.CORS_ORIGINS = get_cors_origins()


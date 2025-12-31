"""
Main FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.config import settings
from app.middleware.audit_middleware import AuditMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.api.v1 import auth, users, banks, credit_reports, credit_data, inquiries, disputes, consumers, audit
from app.database import engine, Base

# Initialize Sentry if enabled
if settings.ENABLE_SENTRY and settings.SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.fastapi import FastApiIntegration
    from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
    
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        integrations=[
            FastApiIntegration(),
            SqlalchemyIntegration(),
        ],
        traces_sample_rate=0.1 if settings.ENVIRONMENT == "production" else 1.0,
        environment=settings.ENVIRONMENT,
    )

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Credit Bureau System API for Marshall Islands",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Rate limiting middleware (must be first)
app.add_middleware(RateLimitMiddleware)

# Audit middleware
app.add_middleware(AuditMiddleware)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted host middleware (for production)
if settings.ENVIRONMENT == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["creditcheck.mh", "*.creditcheck.mh"]
    )

# Include API routers
app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["Authentication"])
app.include_router(users.router, prefix=f"{settings.API_V1_PREFIX}/users", tags=["Users"])
app.include_router(banks.router, prefix=f"{settings.API_V1_PREFIX}/banks", tags=["Banks"])
app.include_router(credit_reports.router, prefix=f"{settings.API_V1_PREFIX}/credit-reports", tags=["Credit Reports"])
app.include_router(credit_data.router, prefix=f"{settings.API_V1_PREFIX}/credit-data", tags=["Credit Data"])
app.include_router(inquiries.router, prefix=f"{settings.API_V1_PREFIX}/inquiries", tags=["Inquiries"])
app.include_router(disputes.router, prefix=f"{settings.API_V1_PREFIX}/disputes", tags=["Disputes"])
app.include_router(consumers.router, prefix=f"{settings.API_V1_PREFIX}/consumers", tags=["Consumers"])
app.include_router(audit.router, prefix=f"{settings.API_V1_PREFIX}/audit", tags=["Audit"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Credit Check API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Quick Start Guide

## What Has Been Created

A complete credit bureau system for the Marshall Islands with:

### Backend (FastAPI/Python)
- ✅ Complete REST API with 9 main endpoints
- ✅ Authentication & Authorization (JWT)
- ✅ User, Bank, Consumer management
- ✅ Credit data submission and management
- ✅ Credit report generation with scoring
- ✅ Credit inquiry system
- ✅ Dispute management
- ✅ Comprehensive audit logging
- ✅ Security features (encryption, hashing, RBAC)

### Frontend (React/TypeScript)
- ✅ Modern React application with TypeScript
- ✅ Authentication UI
- ✅ Basic dashboard
- ✅ Material-UI components
- ✅ API integration

### Infrastructure
- ✅ Docker Compose setup
- ✅ Database models (PostgreSQL)
- ✅ Migration system (Alembic)
- ✅ Redis integration ready

## Quick Start (5 Steps)

### 1. Install Prerequisites

```bash
# Python 3.11+
python --version

# Node.js 18+
node --version

# PostgreSQL 14+
psql --version

# Redis 7+
redis-cli --version
```

### 2. Set Up Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env
# Edit .env with your settings (see SETUP.md)
```

### 3. Set Up Database

```bash
# Create database (in PostgreSQL)
createdb creditcheck

# Run migrations
alembic upgrade head
```

### 4. Set Up Frontend

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env
# Edit .env if needed
```

### 5. Start Services

**Option A: Docker Compose (Easiest)**
```bash
docker-compose up -d
```

**Option B: Manual**
```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Redis (if not using Docker)
redis-server
```

## First Time Setup

### Create Admin User

After starting the backend, create your first admin user:

```python
# Using Python
from app.database import SessionLocal
from app.models.user import User, UserRole
from app.utils.security import get_password_hash

db = SessionLocal()
admin = User(
    email="admin@creditcheck.mh",
    password_hash=get_password_hash("changeme123"),
    full_name="System Administrator",
    role=UserRole.ADMIN,
    is_active=True,
    is_verified=True
)
db.add(admin)
db.commit()
print("Admin user created!")
```

Or use the API:
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@creditcheck.mh",
    "password": "changeme123",
    "full_name": "System Administrator",
    "role": "ADMIN"
  }'
```

## Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Default Login

- Email: `admin@creditcheck.mh`
- Password: `changeme123` (change immediately!)

## Important Environment Variables

### Backend (.env)
```env
SECRET_KEY=your-32-character-secret-key-here
ENCRYPTION_KEY=your-32-byte-encryption-key-here

# Database (Supabase recommended)
DATABASE_URL=postgresql://postgres.[PROJECT]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres

# Redis (Optional - leave empty to disable)
REDIS_URL=
USE_REDIS=false

# Email (Resend)
RESEND_API_KEY=re_xxxxxxxxxxxxx
EMAIL_FROM=noreply@yourdomain.com

# Sentry (Optional)
SENTRY_DSN=
ENABLE_SENTRY=false
```

Generate keys:
```bash
# SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# ENCRYPTION_KEY
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

## Common Issues

### Database Connection Error
- Check PostgreSQL is running: `pg_isready`
- Verify DATABASE_URL in .env
- Ensure database exists: `createdb creditcheck`

### Redis Connection Error
- Redis is optional - you can disable it by setting `USE_REDIS=false` and leaving `REDIS_URL` empty
- If using Redis: Check Redis is running: `redis-cli ping`
- Verify REDIS_URL in .env

### Import Errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again
- Check Python version (3.11+)

### Frontend Not Loading
- Check backend is running on port 8000
- Verify VITE_API_URL in frontend/.env
- Check browser console for errors

## Next Steps

1. **Change default passwords** immediately
2. **Create test banks** via admin panel
3. **Create test consumers** and credit data
4. **Test credit report generation**
5. **Review security settings** before production
6. **Set up backups** for database
7. **Configure monitoring** and logging

## Documentation

- **SETUP.md**: Detailed setup instructions
- **API.md**: Complete API documentation
- **README.md**: Project overview
- **IMPLEMENTATION_STATUS.md**: What's done and what's next

## Support

For detailed instructions, see:
- `SETUP.md` for manual configuration steps
- `docs/API.md` for API endpoint documentation
- `IMPLEMENTATION_STATUS.md` for development status

## Production Checklist

Before deploying to production:

- [ ] Change all default passwords
- [ ] Generate strong SECRET_KEY and ENCRYPTION_KEY
- [ ] Set ENVIRONMENT=production
- [ ] Set DEBUG=False
- [ ] Configure HTTPS/TLS
- [ ] Set up proper CORS origins
- [ ] Configure database backups
- [ ] Set up monitoring
- [ ] Review security settings
- [ ] Conduct security audit
- [ ] Test all functionality
- [ ] Set up CI/CD pipeline


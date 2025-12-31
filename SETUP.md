# Credit Check Application - Setup Instructions

## Manual Steps Required

This document outlines the steps you need to complete manually to get the application running.

### 1. Environment Setup

#### Backend Environment Variables

1. Copy `backend/.env.example` to `backend/.env`
2. Update the following values in `backend/.env`:
   - `SECRET_KEY`: Generate a secure random string (minimum 32 characters)
     ```bash
     python -c "import secrets; print(secrets.token_urlsafe(32))"
     ```
   - `ENCRYPTION_KEY`: Generate a 32-byte key for AES encryption
     ```bash
     python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
     ```
   - `DATABASE_URL`: 
     - **Option A (Supabase - Recommended)**: Use your Supabase connection string
       ```
       DATABASE_URL=postgresql://postgres.[PROJECT]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
       ```
     - **Option B (Local PostgreSQL)**: `postgresql://user:password@localhost:5432/creditcheck`
   - `REDIS_URL`: Leave empty to disable Redis (optional)
   - `RESEND_API_KEY`: Get from https://resend.com/api-keys (recommended for email)
   - `EMAIL_FROM`: Your verified email domain (e.g., `noreply@yourdomain.com`)
   - `SENTRY_DSN`: Get from https://sentry.io (optional, for error tracking)

#### Frontend Environment Variables

1. Copy `frontend/.env.example` to `frontend/.env`
2. Update `VITE_API_URL` to match your backend URL

### 2. Database Setup

#### Install PostgreSQL

- **Windows**: Download from https://www.postgresql.org/download/windows/
- **macOS**: `brew install postgresql`
- **Linux**: `sudo apt-get install postgresql` (Ubuntu/Debian)

#### Create Database

```sql
CREATE DATABASE creditcheck;
CREATE USER creditcheck WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE creditcheck TO creditcheck;
```

#### Run Migrations

```bash
cd backend
alembic upgrade head
```

If this is the first time, create the initial migration:

```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 3. Redis Setup

#### Install Redis

- **Windows**: Download from https://github.com/microsoftarchive/redis/releases or use WSL
- **macOS**: `brew install redis`
- **Linux**: `sudo apt-get install redis-server`

#### Start Redis

```bash
redis-server
```

### 4. Backend Setup

#### Install Python Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Create Initial Admin User

You'll need to create the first admin user manually. You can do this by:

1. Running a Python script:
```python
from app.database import SessionLocal
from app.models.user import User, UserRole
from app.utils.security import get_password_hash

db = SessionLocal()
admin = User(
    email="admin@creditcheck.mh",
    password_hash=get_password_hash("changeme"),
    full_name="System Administrator",
    role=UserRole.ADMIN,
    is_active=True,
    is_verified=True
)
db.add(admin)
db.commit()
```

Or use the API after starting the server:
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@creditcheck.mh",
    "password": "changeme",
    "full_name": "System Administrator",
    "role": "ADMIN"
  }'
```

### 5. Frontend Setup

#### Install Node.js Dependencies

```bash
cd frontend
npm install
```

### 6. Running the Application

#### Option 1: Docker Compose (Recommended)

```bash
docker-compose up -d
```

This will start:
- PostgreSQL on port 5432
- Redis on port 6379
- Backend API on port 8000
- Frontend on port 3000

#### Option 2: Manual Start

**Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm run dev
```

### 7. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 8. Initial Configuration

1. **Login** with the admin account you created
2. **Create Banks**: Use the admin panel to register banks
3. **Approve Banks**: Approve registered banks
4. **Create Users**: Create users for each bank
5. **Configure Settings**: Set up system-wide settings

### 9. Security Checklist

Before going to production:

- [ ] Change all default passwords
- [ ] Use strong SECRET_KEY (minimum 32 characters)
- [ ] Use strong ENCRYPTION_KEY (32 bytes)
- [ ] Enable HTTPS/TLS
- [ ] Configure CORS properly for production
- [ ] Set up proper firewall rules
- [ ] Configure database backups
- [ ] Set up monitoring and logging
- [ ] Review and update rate limiting
- [ ] Enable two-factor authentication
- [ ] Conduct security audit

### 10. Production Deployment

#### Backend Deployment

1. Set `ENVIRONMENT=production` in `.env`
2. Set `DEBUG=False`
3. Use a production WSGI server (e.g., Gunicorn with Uvicorn workers)
4. Set up reverse proxy (Nginx)
5. Configure SSL certificates

#### Frontend Deployment

1. Build the frontend: `npm run build`
2. Serve the `dist` folder with a web server (Nginx, Apache, etc.)
3. Configure API proxy if needed

### 11. Testing

#### Backend Tests

```bash
cd backend
pytest
```

#### Frontend Tests

```bash
cd frontend
npm test
```

### 12. Troubleshooting

#### Database Connection Issues

- Verify PostgreSQL is running: `pg_isready`
- Check connection string in `.env`
- Verify database exists and user has permissions

#### Redis Connection Issues

- Verify Redis is running: `redis-cli ping`
- Check Redis URL in `.env`

#### API Not Responding

- Check backend logs
- Verify all environment variables are set
- Check database migrations ran successfully

#### Frontend Not Loading

- Check browser console for errors
- Verify `VITE_API_URL` is correct
- Check CORS settings in backend

### 13. Next Steps

1. Review the API documentation at `/docs`
2. Test all endpoints
3. Create test data
4. Set up CI/CD pipeline
5. Configure monitoring
6. Set up backups
7. Plan for scaling

## Support

For issues or questions, refer to the main README.md or contact the development team.


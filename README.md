# Credit Check Application - Marshall Islands Credit Bureau

A comprehensive credit bureau system for the Marshall Islands that enables banks and lenders to submit credit data, query consumer credit reports (with consent), manage user access, and handle consumer disputes.

## Architecture

- **Backend**: Python FastAPI (RESTful API)
- **Frontend**: React with TypeScript
- **Database**: PostgreSQL
- **Cache**: Redis
- **Authentication**: JWT with OAuth 2.0
- **Deployment**: Docker containers

## Features

- Role-based access control (ADMIN, BANK_MANAGER, BANK_USER, DATA_PROVIDER, AUDITOR, CONSUMER)
- Secure credit data submission and management
- Credit report generation with consent verification
- Credit inquiry system with audit trails
- Consumer self-service portal
- Dispute management system
- Comprehensive audit logging
- Credit score calculation

## Project Structure

```
credit-check/
├── backend/          # FastAPI backend application
├── frontend/         # React frontend application
├── docker-compose.yml
└── docs/            # Documentation
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis 7+
- Docker and Docker Compose (optional)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run database migrations:
```bash
alembic upgrade head
```

6. Start the development server:
```bash
uvicorn app.main:app --reload
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API URL
```

4. Start the development server:
```bash
npm run dev
```

### Docker Setup (Recommended)

1. Start all services:
```bash
docker-compose up -d
```

2. Run migrations:
```bash
docker-compose exec backend alembic upgrade head
```

3. Access the application:
- Backend API: http://localhost:8000
- Frontend: http://localhost:3000
- API Documentation: http://localhost:8000/docs

## Environment Variables

See `.env.example` files in both `backend/` and `frontend/` directories for required environment variables.

**Quick Setup:**
- Use **Supabase** for database (free tier) - see `docs/SUPABASE_SETUP.md`
- Use **Resend** for email (free tier: 3,000 emails/month)
- Use **Sentry** for error tracking (free tier: 5,000 errors/month)
- **Redis is optional** - can be disabled initially

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Security

- All sensitive data is encrypted at rest (AES-256)
- TLS 1.3 for data in transit
- JWT tokens with short expiration times
- Two-factor authentication for admin and bank users
- Rate limiting on all API endpoints
- Comprehensive audit logging

## Documentation

- API Documentation: Available at `/docs` endpoint when backend is running
- User Guides: See `docs/` directory
- Architecture: See `docs/architecture.md`

## License

Proprietary - Marshall Islands Credit Bureau

## Support

For issues and questions, please contact the development team.


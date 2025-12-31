# Deployment Guide

## Recommended Cloud Stack (Cost-Optimized)

This guide covers deploying the Credit Check application using modern, cost-effective cloud services.

### Stack Overview

```
Database:     Supabase (Free tier) ✅
Backend:      Railway / Render ($5-10/month)
Frontend:     Vercel (Free tier) ✅
Email:        Resend (Free tier) ✅
Monitoring:   Sentry (Free tier) ✅
Redis:        Optional (skip initially)
```

**Total Monthly Cost: ~$5-10**

## Step-by-Step Deployment

### 1. Database Setup (Supabase)

#### Create Supabase Project

1. Go to https://supabase.com
2. Sign up for free account
3. Create new project
4. Note your project credentials:
   - Database URL (Connection string)
   - API keys (if needed)

#### Get Connection String

1. Go to Project Settings → Database
2. Copy the "Connection string" under "Connection string"
3. Format: `postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres`

#### Update Environment Variables

```env
DATABASE_URL=postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
```

#### Run Migrations

```bash
cd backend
alembic upgrade head
```

### 2. Backend Deployment (Railway or Render)

#### Option A: Railway (Recommended)

1. **Sign up**: https://railway.app
2. **Create Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo" (or upload code)
3. **Configure Environment Variables**:
   ```
   DATABASE_URL=<from-supabase>
   SECRET_KEY=<generate-strong-key>
   ENCRYPTION_KEY=<generate-32-byte-key>
   RESEND_API_KEY=<from-resend>
   EMAIL_FROM=noreply@yourdomain.com
   SENTRY_DSN=<from-sentry>
   ENABLE_SENTRY=true
   CORS_ORIGINS=https://your-frontend.vercel.app
   ENVIRONMENT=production
   DEBUG=false
   ```
4. **Deploy**: Railway will auto-detect FastAPI and deploy

#### Option B: Render

1. **Sign up**: https://render.com
2. **Create Web Service**:
   - Connect GitHub repo
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. **Add Environment Variables** (same as Railway)
4. **Deploy**: Render will build and deploy

### 3. Frontend Deployment (Vercel)

1. **Sign up**: https://vercel.com
2. **Import Project**:
   - Connect GitHub repo
   - Select `frontend` folder
3. **Configure Environment Variables**:
   ```
   VITE_API_URL=https://your-backend.railway.app
   ```
4. **Deploy**: Vercel will auto-detect Vite and deploy

### 4. Email Service (Resend)

1. **Sign up**: https://resend.com
2. **Get API Key**:
   - Go to API Keys
   - Create new key
   - Copy the key
3. **Verify Domain** (for production):
   - Add your domain
   - Add DNS records
   - Verify domain
4. **Update Environment**:
   ```env
   RESEND_API_KEY=re_xxxxxxxxxxxxx
   EMAIL_FROM=noreply@yourdomain.com
   ```

### 5. Error Tracking (Sentry)

1. **Sign up**: https://sentry.io
2. **Create Project**:
   - Select "FastAPI"
   - Copy DSN
3. **Update Environment**:
   ```env
   SENTRY_DSN=https://xxx@xxx.ingest.sentry.io/xxx
   ENABLE_SENTRY=true
   ```

### 6. Domain & SSL

#### Option A: Use Vercel Domain (Free)

- Vercel provides free SSL
- Use provided domain: `your-app.vercel.app`

#### Option B: Custom Domain

1. **Buy Domain**: Namecheap, Google Domains, etc.
2. **Configure DNS**:
   - Add CNAME for frontend: `www` → `your-app.vercel.app`
   - Add A record for API: `api` → Railway/Render IP
3. **SSL**: Automatically handled by Vercel and Railway/Render

## Environment Variables Checklist

### Backend (.env)

```env
# Application
ENVIRONMENT=production
DEBUG=false
API_V1_PREFIX=/api/v1

# Database (Supabase)
DATABASE_URL=postgresql://postgres.[PROJECT]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres

# Redis (Optional - leave empty to disable)
REDIS_URL=
USE_REDIS=false

# Security
SECRET_KEY=<generate-32-char-minimum>
ENCRYPTION_KEY=<generate-32-byte-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=https://your-frontend.vercel.app,https://www.yourdomain.com

# Email (Resend)
RESEND_API_KEY=re_xxxxxxxxxxxxx
EMAIL_FROM=noreply@yourdomain.com
USE_SMTP=false

# Sentry
SENTRY_DSN=https://xxx@xxx.ingest.sentry.io/xxx
ENABLE_SENTRY=true

# Logging
LOG_LEVEL=INFO
```

### Frontend (.env)

```env
VITE_API_URL=https://your-backend.railway.app
VITE_APP_NAME=Credit Check
```

## Post-Deployment Checklist

- [ ] Database migrations run successfully
- [ ] Backend API accessible at `/health`
- [ ] Frontend loads correctly
- [ ] Can login with admin account
- [ ] Email sending works (test verification email)
- [ ] Sentry error tracking works (test by triggering error)
- [ ] SSL certificates active (HTTPS)
- [ ] CORS configured correctly
- [ ] Environment variables set correctly
- [ ] Backups configured (Supabase auto-backups)
- [ ] Monitoring set up (Sentry)

## Cost Breakdown

### Free Tier Services
- **Supabase**: 500MB database, 2GB bandwidth
- **Vercel**: Unlimited static hosting
- **Resend**: 3,000 emails/month
- **Sentry**: 5,000 errors/month

### Paid Services
- **Railway/Render**: $5-10/month (backend hosting)
- **Domain**: $10-15/year (optional)

**Total: ~$5-10/month**

## Scaling Considerations

### When to Add Redis

Add Redis when you need:
- High-performance rate limiting (>1000 req/min)
- Caching credit scores/reports
- Real-time features
- Background job queues

**Options:**
- Upstash Redis (serverless, pay-per-use)
- Railway Redis addon
- Supabase Edge Functions (alternative)

### Database Scaling

Supabase free tier limits:
- 500MB database
- 2GB bandwidth/month

**Upgrade when:**
- Database > 400MB
- Approaching bandwidth limits
- Need more connections

**Supabase Pro**: $25/month (8GB database, 50GB bandwidth)

## Monitoring & Maintenance

### Daily
- Check Sentry for errors
- Monitor API response times

### Weekly
- Review audit logs
- Check database size
- Review email delivery rates

### Monthly
- Review costs
- Check for security updates
- Backup verification

## Troubleshooting

### Backend Not Starting
- Check environment variables
- Verify database connection
- Check logs in Railway/Render dashboard

### Database Connection Issues
- Verify Supabase connection string
- Check IP allowlist in Supabase
- Test connection with `psql`

### Email Not Sending
- Verify Resend API key
- Check domain verification
- Review Resend dashboard for errors

### Frontend API Errors
- Verify `VITE_API_URL` is correct
- Check CORS settings
- Verify backend is running

## Security Best Practices

1. **Never commit `.env` files**
2. **Use strong SECRET_KEY** (32+ characters)
3. **Rotate API keys regularly**
4. **Enable 2FA on all services**
5. **Use HTTPS everywhere**
6. **Regular security audits**
7. **Monitor Sentry for suspicious activity**
8. **Keep dependencies updated**

## Backup Strategy

### Supabase Backups
- Automatic daily backups (free tier)
- 7-day retention
- Manual backup available

### Code Backups
- GitHub repository (primary)
- Regular local backups

### Database Backups
```bash
# Manual backup
pg_dump $DATABASE_URL > backup.sql

# Restore
psql $DATABASE_URL < backup.sql
```

## Support Resources

- **Supabase Docs**: https://supabase.com/docs
- **Railway Docs**: https://docs.railway.app
- **Vercel Docs**: https://vercel.com/docs
- **Resend Docs**: https://resend.com/docs
- **Sentry Docs**: https://docs.sentry.io


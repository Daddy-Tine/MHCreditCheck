# Supabase Setup Guide

## Why Supabase?

Supabase provides a managed PostgreSQL database that's:
- **Free** for small projects (500MB database, 2GB bandwidth)
- **Fully compatible** with our PostgreSQL code (no changes needed)
- **Easy to use** with web dashboard
- **Auto-scales** when you need more

## Step 1: Create Supabase Account

1. Go to https://supabase.com
2. Click "Start your project"
3. Sign up with GitHub (recommended) or email
4. Verify your email

## Step 2: Create New Project

1. Click "New Project"
2. Fill in:
   - **Name**: Credit Check (or your preferred name)
   - **Database Password**: Generate a strong password (save it!)
   - **Region**: Choose closest to Marshall Islands (or your users)
   - **Pricing Plan**: Free (to start)
3. Click "Create new project"
4. Wait 2-3 minutes for project to initialize

## Step 3: Get Connection String

1. Go to **Project Settings** (gear icon)
2. Click **Database** in left sidebar
3. Scroll to **Connection string**
4. Select **URI** tab
5. Copy the connection string

It looks like:
```
postgresql://postgres.[PROJECT-REF]:[YOUR-PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
```

**Important**: Replace `[YOUR-PASSWORD]` with the password you set when creating the project.

## Step 4: Update Your .env File

```env
DATABASE_URL=postgresql://postgres.[PROJECT-REF]:[YOUR-PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
```

## Step 5: Run Migrations

```bash
cd backend
alembic upgrade head
```

This will create all your database tables in Supabase.

## Step 6: Verify Setup

1. Go to Supabase dashboard
2. Click **Table Editor** in left sidebar
3. You should see all your tables:
   - users
   - banks
   - consumers
   - credit_accounts
   - credit_reports
   - credit_inquiries
   - disputes
   - audit_logs
   - consents

## Using Supabase Dashboard

### View Data

1. Go to **Table Editor**
2. Click on any table
3. View, edit, or add rows directly

### Run SQL Queries

1. Go to **SQL Editor**
2. Write SQL queries
3. Click "Run" to execute

Example:
```sql
SELECT * FROM users WHERE role = 'ADMIN';
```

### Monitor Usage

1. Go to **Settings** → **Usage**
2. See database size, bandwidth, etc.

## Security Best Practices

### 1. Enable Row Level Security (Optional)

Supabase supports Row Level Security (RLS) for additional security:

```sql
-- Example: Only allow users to see their own data
ALTER TABLE consumers ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own data"
ON consumers
FOR SELECT
USING (user_id = auth.uid());
```

### 2. Connection Pooling

Use the **pooler** connection string (port 6543) for better performance:
```
postgresql://postgres.[PROJECT]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
```

### 3. IP Restrictions (Production)

1. Go to **Settings** → **Database**
2. Add your server IPs to allowlist
3. Or use connection pooling (recommended)

## Backup & Restore

### Automatic Backups

- Supabase automatically backs up daily
- 7-day retention (free tier)
- Go to **Settings** → **Database** → **Backups** to view

### Manual Backup

```bash
# Backup
pg_dump $DATABASE_URL > backup.sql

# Restore
psql $DATABASE_URL < backup.sql
```

## Scaling

### Free Tier Limits
- 500MB database
- 2GB bandwidth/month
- 2GB file storage
- 50,000 monthly active users

### When to Upgrade

Upgrade to **Pro** ($25/month) when:
- Database > 400MB
- Approaching bandwidth limits
- Need more storage
- Need longer backup retention

### Pro Tier Benefits
- 8GB database
- 50GB bandwidth/month
- 100GB file storage
- 30-day backup retention
- Daily backups

## Troubleshooting

### Connection Timeout

**Problem**: Can't connect to database

**Solutions**:
1. Check connection string is correct
2. Verify password is correct
3. Check if project is paused (free tier pauses after 1 week inactivity)
4. Use connection pooler (port 6543)

### Migration Errors

**Problem**: `alembic upgrade head` fails

**Solutions**:
1. Check DATABASE_URL is correct
2. Verify database password
3. Check Supabase project is active
4. Review error message for specific issue

### Slow Queries

**Problem**: Database queries are slow

**Solutions**:
1. Use connection pooler (port 6543)
2. Add database indexes (already in migrations)
3. Check query performance in SQL Editor
4. Consider upgrading to Pro tier

## Migration from Local PostgreSQL

If you're moving from local PostgreSQL to Supabase:

1. **Backup local database**:
   ```bash
   pg_dump local_db > backup.sql
   ```

2. **Create Supabase project** (see above)

3. **Restore to Supabase**:
   ```bash
   psql $SUPABASE_DATABASE_URL < backup.sql
   ```

4. **Update .env** with Supabase connection string

5. **Test** all functionality

## Additional Supabase Features (Optional)

### Edge Functions

Supabase Edge Functions can replace some backend logic:
- Serverless functions
- Automatic scaling
- Built-in authentication

### Storage

Use Supabase Storage for:
- File uploads
- Document storage
- Images

### Real-time

Enable real-time subscriptions:
- Live updates
- WebSocket connections
- Push notifications

## Support

- **Supabase Docs**: https://supabase.com/docs
- **Supabase Discord**: https://discord.supabase.com
- **Supabase GitHub**: https://github.com/supabase/supabase

## Next Steps

After setting up Supabase:
1. ✅ Run migrations
2. ✅ Create initial admin user
3. ✅ Test database connections
4. ✅ Set up backups (automatic)
5. ✅ Monitor usage dashboard


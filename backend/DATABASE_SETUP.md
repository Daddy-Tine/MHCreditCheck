# Database Connection Setup Guide

## Quick Start

### 1. Test Database Connection

Run the connection test script:

```powershell
cd backend
.\test_connection.ps1
```

This will:
- Set up a virtual environment (if needed)
- Install dependencies
- Test the database connection
- Show current migration status
- List all tables

### 2. Run Migrations

After confirming the connection works:

```powershell
cd backend
.\run_migrations.ps1
```

This will:
- Run all pending migrations
- Create all database tables
- Show the current migration version

## Manual Setup

### Option 1: Environment Variable (Recommended)

Set the `DATABASE_URL` environment variable:

**PowerShell:**
```powershell
$env:DATABASE_URL = "postgresql://postgres:dR3gnpfOWidZUnvo@db.qejqdwzfemhtrgcnotid.supabase.co:5432/postgres"
```

**CMD:**
```cmd
set DATABASE_URL=postgresql://postgres:dR3gnpfOWidZUnvo@db.qejqdwzfemhtrgcnotid.supabase.co:5432/postgres
```

Then run:
```bash
cd backend
alembic upgrade head
```

### Option 2: .env File

Create `backend/.env`:

```env
DATABASE_URL=postgresql://postgres:dR3gnpfOWidZUnvo@db.qejqdwzfemhtrgcnotid.supabase.co:5432/postgres
SECRET_KEY=your-secret-key-here
ENCRYPTION_KEY=your-32-byte-encryption-key-here
```

## Automatic Migrations

### GitHub Actions

Migrations run automatically when you:
- Push to `main` or `master` branch
- Change files in `backend/alembic/versions/` or `backend/app/models/`
- Manually trigger the workflow

The workflow uses the `SUPABASE_DATABASE_URL` secret you added to GitHub.

### View Workflow Status

1. Go to your GitHub repository
2. Click "Actions" tab
3. Select "Run Database Migrations" workflow
4. View the logs to see migration results

## Verification

### Check Connection

```bash
cd backend
python test_db_connection.py
```

### Check Migration Status

```bash
cd backend
alembic current
```

### View All Migrations

```bash
cd backend
alembic history
```

## Troubleshooting

### Connection Failed

1. **Check Supabase project is active**
   - Free tier projects pause after 1 week of inactivity
   - Go to Supabase dashboard and reactivate if needed

2. **Verify connection string**
   - Check password is correct
   - Ensure project reference is correct
   - Try connection pooler URL if direct connection fails

3. **Check network connectivity**
   - Some networks block direct database connections
   - Use connection pooler (port 6543) instead

### Migration Errors

1. **Check DATABASE_URL is set**
   ```bash
   echo $DATABASE_URL  # Linux/Mac
   echo %DATABASE_URL%  # Windows CMD
   $env:DATABASE_URL  # PowerShell
   ```

2. **Verify database is accessible**
   - Run connection test first
   - Check Supabase dashboard

3. **Review error messages**
   - Check Alembic output for specific errors
   - Verify all models are imported correctly

### IPv4 Compatibility

If you see "Not IPv4 compatible" warning:
- Use connection pooler URL (port 6543)
- Or purchase IPv4 add-on in Supabase

## Security Notes

⚠️ **Never commit connection strings to Git!**

- The scripts (`test_connection.ps1`, `run_migrations.ps1`) contain your password
- They are in `.gitignore` but be careful
- Use environment variables or GitHub Secrets for production
- Rotate passwords regularly

## Next Steps

After successful connection and migrations:

1. ✅ Verify tables in Supabase dashboard
2. ✅ Create initial admin user
3. ✅ Test API endpoints
4. ✅ Set up monitoring


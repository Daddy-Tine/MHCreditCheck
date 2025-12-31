"""
Test script to verify database connection
"""
import os
import sys
from sqlalchemy import create_engine, text
from app.config import settings

def test_connection():
    """Test database connection"""
    print("=" * 60)
    print("Testing Database Connection")
    print("=" * 60)
    
    # Get database URL
    db_url = settings.DATABASE_URL
    print(f"\nDatabase URL: {db_url.split('@')[0]}@[HIDDEN]")
    
    try:
        # Create engine
        print("\n1. Creating database engine...")
        engine = create_engine(db_url, pool_pre_ping=True)
        
        # Test connection
        print("2. Testing connection...")
        with engine.connect() as connection:
            # Test query
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"   ✓ Connected successfully!")
            print(f"   PostgreSQL version: {version.split(',')[0]}")
            
            # Check if alembic_version table exists
            print("\n3. Checking migration status...")
            result = connection.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'alembic_version'
                );
            """))
            has_alembic = result.fetchone()[0]
            
            if has_alembic:
                result = connection.execute(text("SELECT version_num FROM alembic_version ORDER BY version_num DESC LIMIT 1;"))
                current_version = result.fetchone()
                if current_version:
                    print(f"   ✓ Alembic version table exists")
                    print(f"   Current migration version: {current_version[0]}")
                else:
                    print("   ⚠ Alembic table exists but no version found")
            else:
                print("   ⚠ No migrations have been run yet")
                print("   Run: alembic upgrade head")
            
            # Check for our tables
            print("\n4. Checking for application tables...")
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_type = 'BASE TABLE'
                ORDER BY table_name;
            """))
            tables = [row[0] for row in result.fetchall()]
            
            expected_tables = [
                'users', 'banks', 'consumers', 'credit_accounts',
                'credit_reports', 'credit_inquiries', 'disputes',
                'audit_logs', 'consents'
            ]
            
            if tables:
                print(f"   Found {len(tables)} table(s):")
                for table in tables:
                    status = "✓" if table in expected_tables else "?"
                    print(f"   {status} {table}")
                
                missing = set(expected_tables) - set(tables)
                if missing:
                    print(f"\n   ⚠ Missing tables: {', '.join(missing)}")
                    print("   Run migrations: alembic upgrade head")
                else:
                    print("\n   ✓ All expected tables found!")
            else:
                print("   ⚠ No tables found. Run migrations: alembic upgrade head")
        
        print("\n" + "=" * 60)
        print("✓ Database connection test PASSED")
        print("=" * 60)
        return True
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("✗ Database connection test FAILED")
        print("=" * 60)
        print(f"\nError: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Check DATABASE_URL is set correctly")
        print("2. Verify Supabase project is active")
        print("3. Check password is correct")
        print("4. Verify network connectivity")
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)


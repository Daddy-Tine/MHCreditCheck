"""Initial migration: create all tables

Revision ID: 001_initial
Revises: 
Create Date: 2025-01-27 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create ENUM types (only if they don't exist)
    # Using IF NOT EXISTS check - if type exists, skip creation
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'userrole') THEN
                CREATE TYPE userrole AS ENUM ('ADMIN', 'BANK_MANAGER', 'BANK_USER', 'DATA_PROVIDER', 'AUDITOR', 'CONSUMER');
            END IF;
        EXCEPTION WHEN OTHERS THEN NULL;
        END$$;
    """)
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'accounttype') THEN
                CREATE TYPE accounttype AS ENUM ('CREDIT_CARD', 'MORTGAGE', 'AUTO_LOAN', 'PERSONAL_LOAN', 'STUDENT_LOAN', 'LINE_OF_CREDIT', 'OTHER');
            END IF;
        EXCEPTION WHEN OTHERS THEN NULL;
        END$$;
    """)
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'accountstatus') THEN
                CREATE TYPE accountstatus AS ENUM ('OPEN', 'CLOSED', 'DELINQUENT', 'CHARGE_OFF', 'COLLECTION', 'BANKRUPTCY');
            END IF;
        EXCEPTION WHEN OTHERS THEN NULL;
        END$$;
    """)
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'paymentstatus') THEN
                CREATE TYPE paymentstatus AS ENUM ('CURRENT', 'LATE_30', 'LATE_60', 'LATE_90', 'LATE_120_PLUS', 'NO_PAYMENT');
            END IF;
        EXCEPTION WHEN OTHERS THEN NULL;
        END$$;
    """)
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'inquirypurpose') THEN
                CREATE TYPE inquirypurpose AS ENUM ('LOAN_APPLICATION', 'CREDIT_CARD_APPLICATION', 'EMPLOYMENT', 'RENTAL_APPLICATION', 'INSURANCE', 'ACCOUNT_REVIEW', 'OTHER');
            END IF;
        EXCEPTION WHEN OTHERS THEN NULL;
        END$$;
    """)
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'inquirystatus') THEN
                CREATE TYPE inquirystatus AS ENUM ('PENDING', 'APPROVED', 'DENIED', 'CANCELLED');
            END IF;
        EXCEPTION WHEN OTHERS THEN NULL;
        END$$;
    """)
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'disputestatus') THEN
                CREATE TYPE disputestatus AS ENUM ('PENDING', 'UNDER_REVIEW', 'RESOLVED', 'REJECTED', 'WITHDRAWN');
            END IF;
        EXCEPTION WHEN OTHERS THEN NULL;
        END$$;
    """)
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'disputereason') THEN
                CREATE TYPE disputereason AS ENUM ('INCORRECT_BALANCE', 'INCORRECT_PAYMENT_HISTORY', 'ACCOUNT_NOT_MINE', 'DUPLICATE_ACCOUNT', 'FRAUD', 'IDENTITY_THEFT', 'OTHER');
            END IF;
        EXCEPTION WHEN OTHERS THEN NULL;
        END$$;
    """)
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'auditaction') THEN
                CREATE TYPE auditaction AS ENUM ('CREATE', 'READ', 'UPDATE', 'DELETE', 'LOGIN', 'LOGOUT', 'LOGIN_FAILED', 'PERMISSION_DENIED', 'DATA_EXPORT', 'PASSWORD_CHANGE', 'ACCOUNT_LOCKED');
            END IF;
        EXCEPTION WHEN OTHERS THEN NULL;
        END$$;
    """)
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'consenttype') THEN
                CREATE TYPE consenttype AS ENUM ('CREDIT_REPORT', 'DATA_SHARING', 'MARKETING');
            END IF;
        EXCEPTION WHEN OTHERS THEN NULL;
        END$$;
    """)
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'consentstatus') THEN
                CREATE TYPE consentstatus AS ENUM ('GRANTED', 'REVOKED', 'EXPIRED');
            END IF;
        EXCEPTION WHEN OTHERS THEN NULL;
        END$$;
    """)

    # Create banks table (no dependencies)
    op.create_table(
        'banks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('license_number', sa.String(length=100), nullable=False),
        sa.Column('tax_id', sa.String(length=100), nullable=True),
        sa.Column('contact_email', sa.String(length=255), nullable=False),
        sa.Column('contact_phone', sa.String(length=50), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('api_key', sa.String(length=255), nullable=True),
        sa.Column('api_key_hash', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('is_approved', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('approved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('approved_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_banks_id'), 'banks', ['id'], unique=False)
    op.create_index(op.f('ix_banks_name'), 'banks', ['name'], unique=False)
    op.create_index(op.f('ix_banks_license_number'), 'banks', ['license_number'], unique=True)
    op.create_index(op.f('ix_banks_tax_id'), 'banks', ['tax_id'], unique=True)
    op.create_index(op.f('ix_banks_api_key'), 'banks', ['api_key'], unique=True)

    # Create users table (depends on banks)
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('role', postgresql.ENUM('ADMIN', 'BANK_MANAGER', 'BANK_USER', 'DATA_PROVIDER', 'AUDITOR', 'CONSUMER', name='userrole'), nullable=False),
        sa.Column('bank_id', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('is_verified', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('two_factor_enabled', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('two_factor_secret', sa.String(length=255), nullable=True),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['bank_id'], ['banks.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_role'), 'users', ['role'], unique=False)
    op.create_index(op.f('ix_users_bank_id'), 'users', ['bank_id'], unique=False)

    # Create consumers table
    op.create_table(
        'consumers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ssn_encrypted', sa.String(length=512), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=False),
        sa.Column('last_name', sa.String(length=100), nullable=False),
        sa.Column('middle_name', sa.String(length=100), nullable=True),
        sa.Column('date_of_birth', sa.Date(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('city', sa.String(length=100), nullable=True),
        sa.Column('state', sa.String(length=100), nullable=True),
        sa.Column('zip_code', sa.String(length=20), nullable=True),
        sa.Column('country', sa.String(length=100), server_default='Marshall Islands', nullable=False),
        sa.Column('is_frozen', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_consumers_id'), 'consumers', ['id'], unique=False)
    op.create_index(op.f('ix_consumers_ssn_encrypted'), 'consumers', ['ssn_encrypted'], unique=True)
    op.create_index(op.f('ix_consumers_first_name'), 'consumers', ['first_name'], unique=False)
    op.create_index(op.f('ix_consumers_last_name'), 'consumers', ['last_name'], unique=False)
    op.create_index(op.f('ix_consumers_date_of_birth'), 'consumers', ['date_of_birth'], unique=False)
    op.create_index(op.f('ix_consumers_email'), 'consumers', ['email'], unique=True)
    op.create_index(op.f('ix_consumers_user_id'), 'consumers', ['user_id'], unique=True)

    # Create credit_accounts table (depends on consumers and banks)
    op.create_table(
        'credit_accounts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('consumer_id', sa.Integer(), nullable=False),
        sa.Column('bank_id', sa.Integer(), nullable=False),
        sa.Column('account_number_encrypted', sa.String(length=512), nullable=False),
        sa.Column('account_type', postgresql.ENUM('CREDIT_CARD', 'MORTGAGE', 'AUTO_LOAN', 'PERSONAL_LOAN', 'STUDENT_LOAN', 'LINE_OF_CREDIT', 'OTHER', name='accounttype'), nullable=False),
        sa.Column('account_status', postgresql.ENUM('OPEN', 'CLOSED', 'DELINQUENT', 'CHARGE_OFF', 'COLLECTION', 'BANKRUPTCY', name='accountstatus'), nullable=False),
        sa.Column('payment_status', postgresql.ENUM('CURRENT', 'LATE_30', 'LATE_60', 'LATE_90', 'LATE_120_PLUS', 'NO_PAYMENT', name='paymentstatus'), nullable=False),
        sa.Column('credit_limit', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('current_balance', sa.Numeric(precision=15, scale=2), server_default='0', nullable=False),
        sa.Column('minimum_payment', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('payment_due_date', sa.Date(), nullable=True),
        sa.Column('open_date', sa.Date(), nullable=False),
        sa.Column('close_date', sa.Date(), nullable=True),
        sa.Column('last_payment_date', sa.Date(), nullable=True),
        sa.Column('last_payment_amount', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('months_since_last_payment', sa.Integer(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('is_disputed', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['bank_id'], ['banks.id'], ),
        sa.ForeignKeyConstraint(['consumer_id'], ['consumers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_credit_accounts_id'), 'credit_accounts', ['id'], unique=False)
    op.create_index(op.f('ix_credit_accounts_consumer_id'), 'credit_accounts', ['consumer_id'], unique=False)
    op.create_index(op.f('ix_credit_accounts_bank_id'), 'credit_accounts', ['bank_id'], unique=False)
    op.create_index(op.f('ix_credit_accounts_account_type'), 'credit_accounts', ['account_type'], unique=False)
    op.create_index(op.f('ix_credit_accounts_account_status'), 'credit_accounts', ['account_status'], unique=False)
    op.create_index(op.f('ix_credit_accounts_payment_status'), 'credit_accounts', ['payment_status'], unique=False)

    # Create credit_reports table (depends on consumers and users)
    op.create_table(
        'credit_reports',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('consumer_id', sa.Integer(), nullable=False),
        sa.Column('credit_score', sa.Integer(), nullable=False),
        sa.Column('score_factors', sa.JSON(), nullable=True),
        sa.Column('report_data', sa.JSON(), nullable=False),
        sa.Column('version', sa.Integer(), server_default='1', nullable=False),
        sa.Column('generated_by', sa.Integer(), nullable=True),
        sa.Column('generated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('pdf_path', sa.String(length=512), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['consumer_id'], ['consumers.id'], ),
        sa.ForeignKeyConstraint(['generated_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_credit_reports_id'), 'credit_reports', ['id'], unique=False)
    op.create_index(op.f('ix_credit_reports_consumer_id'), 'credit_reports', ['consumer_id'], unique=False)
    op.create_index(op.f('ix_credit_reports_credit_score'), 'credit_reports', ['credit_score'], unique=False)

    # Create credit_inquiries table (depends on consumers, banks, users, credit_reports)
    op.create_table(
        'credit_inquiries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('consumer_id', sa.Integer(), nullable=False),
        sa.Column('bank_id', sa.Integer(), nullable=False),
        sa.Column('requested_by', sa.Integer(), nullable=False),
        sa.Column('purpose', postgresql.ENUM('LOAN_APPLICATION', 'CREDIT_CARD_APPLICATION', 'EMPLOYMENT', 'RENTAL_APPLICATION', 'INSURANCE', 'ACCOUNT_REVIEW', 'OTHER', name='inquirypurpose'), nullable=False),
        sa.Column('purpose_description', sa.Text(), nullable=True),
        sa.Column('consent_given', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('consent_verified_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', postgresql.ENUM('PENDING', 'APPROVED', 'DENIED', 'CANCELLED', name='inquirystatus'), server_default='PENDING', nullable=False),
        sa.Column('credit_report_id', sa.Integer(), nullable=True),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['bank_id'], ['banks.id'], ),
        sa.ForeignKeyConstraint(['consumer_id'], ['consumers.id'], ),
        sa.ForeignKeyConstraint(['credit_report_id'], ['credit_reports.id'], ),
        sa.ForeignKeyConstraint(['requested_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_credit_inquiries_id'), 'credit_inquiries', ['id'], unique=False)
    op.create_index(op.f('ix_credit_inquiries_consumer_id'), 'credit_inquiries', ['consumer_id'], unique=False)
    op.create_index(op.f('ix_credit_inquiries_bank_id'), 'credit_inquiries', ['bank_id'], unique=False)
    op.create_index(op.f('ix_credit_inquiries_purpose'), 'credit_inquiries', ['purpose'], unique=False)
    op.create_index(op.f('ix_credit_inquiries_status'), 'credit_inquiries', ['status'], unique=False)

    # Create disputes table (depends on consumers, credit_accounts, users)
    op.create_table(
        'disputes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('consumer_id', sa.Integer(), nullable=False),
        sa.Column('credit_account_id', sa.Integer(), nullable=True),
        sa.Column('reason', postgresql.ENUM('INCORRECT_BALANCE', 'INCORRECT_PAYMENT_HISTORY', 'ACCOUNT_NOT_MINE', 'DUPLICATE_ACCOUNT', 'FRAUD', 'IDENTITY_THEFT', 'OTHER', name='disputereason'), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('status', postgresql.ENUM('PENDING', 'UNDER_REVIEW', 'RESOLVED', 'REJECTED', 'WITHDRAWN', name='disputestatus'), server_default='PENDING', nullable=False),
        sa.Column('submitted_by', sa.Integer(), nullable=True),
        sa.Column('reviewed_by', sa.Integer(), nullable=True),
        sa.Column('resolution_notes', sa.Text(), nullable=True),
        sa.Column('resolved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['consumer_id'], ['consumers.id'], ),
        sa.ForeignKeyConstraint(['credit_account_id'], ['credit_accounts.id'], ),
        sa.ForeignKeyConstraint(['reviewed_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['submitted_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_disputes_id'), 'disputes', ['id'], unique=False)
    op.create_index(op.f('ix_disputes_consumer_id'), 'disputes', ['consumer_id'], unique=False)
    op.create_index(op.f('ix_disputes_credit_account_id'), 'disputes', ['credit_account_id'], unique=False)
    op.create_index(op.f('ix_disputes_status'), 'disputes', ['status'], unique=False)

    # Create audit_logs table (depends on users)
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('action', postgresql.ENUM('CREATE', 'READ', 'UPDATE', 'DELETE', 'LOGIN', 'LOGOUT', 'LOGIN_FAILED', 'PERMISSION_DENIED', 'DATA_EXPORT', 'PASSWORD_CHANGE', 'ACCOUNT_LOCKED', name='auditaction'), nullable=False),
        sa.Column('resource_type', sa.String(length=100), nullable=False),
        sa.Column('resource_id', sa.Integer(), nullable=True),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('request_method', sa.String(length=10), nullable=True),
        sa.Column('request_path', sa.String(length=512), nullable=True),
        sa.Column('request_body', sa.JSON(), nullable=True),
        sa.Column('response_status', sa.Integer(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('additional_metadata', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_logs_id'), 'audit_logs', ['id'], unique=False)
    op.create_index(op.f('ix_audit_logs_user_id'), 'audit_logs', ['user_id'], unique=False)
    op.create_index(op.f('ix_audit_logs_action'), 'audit_logs', ['action'], unique=False)
    op.create_index(op.f('ix_audit_logs_resource_type'), 'audit_logs', ['resource_type'], unique=False)
    op.create_index(op.f('ix_audit_logs_resource_id'), 'audit_logs', ['resource_id'], unique=False)
    op.create_index(op.f('ix_audit_logs_created_at'), 'audit_logs', ['created_at'], unique=False)

    # Create consents table (depends on consumers and banks)
    op.create_table(
        'consents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('consumer_id', sa.Integer(), nullable=False),
        sa.Column('consent_type', postgresql.ENUM('CREDIT_REPORT', 'DATA_SHARING', 'MARKETING', name='consenttype'), nullable=False),
        sa.Column('status', postgresql.ENUM('GRANTED', 'REVOKED', 'EXPIRED', name='consentstatus'), server_default='GRANTED', nullable=False),
        sa.Column('bank_id', sa.Integer(), nullable=True),
        sa.Column('purpose', sa.Text(), nullable=True),
        sa.Column('granted_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('revoked_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['bank_id'], ['banks.id'], ),
        sa.ForeignKeyConstraint(['consumer_id'], ['consumers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_consents_id'), 'consents', ['id'], unique=False)
    op.create_index(op.f('ix_consents_consumer_id'), 'consents', ['consumer_id'], unique=False)
    op.create_index(op.f('ix_consents_consent_type'), 'consents', ['consent_type'], unique=False)
    op.create_index(op.f('ix_consents_status'), 'consents', ['status'], unique=False)
    op.create_index(op.f('ix_consents_bank_id'), 'consents', ['bank_id'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('consents')
    op.drop_table('audit_logs')
    op.drop_table('disputes')
    op.drop_table('credit_inquiries')
    op.drop_table('credit_reports')
    op.drop_table('credit_accounts')
    op.drop_table('consumers')
    op.drop_table('users')
    op.drop_table('banks')
    
    # Drop ENUM types
    op.execute('DROP TYPE IF EXISTS consentstatus')
    op.execute('DROP TYPE IF EXISTS consenttype')
    op.execute('DROP TYPE IF EXISTS auditaction')
    op.execute('DROP TYPE IF EXISTS disputereason')
    op.execute('DROP TYPE IF EXISTS disputestatus')
    op.execute('DROP TYPE IF EXISTS inquirystatus')
    op.execute('DROP TYPE IF EXISTS inquirypurpose')
    op.execute('DROP TYPE IF EXISTS paymentstatus')
    op.execute('DROP TYPE IF EXISTS accountstatus')
    op.execute('DROP TYPE IF EXISTS accounttype')
    op.execute('DROP TYPE IF EXISTS userrole')


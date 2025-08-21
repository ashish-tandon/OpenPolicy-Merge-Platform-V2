"""Add missing multi-level government schema components (extending existing comprehensive schema)

Revision ID: 004
Revises: 003
Create Date: 2025-01-27 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # ============================================================================
    # GOVERNMENT LEVEL TRACKING (NEW - Only missing piece)
    # ============================================================================
    
    # Create government_levels table for Federal/Provincial/Municipal classification
    op.create_table('government_levels',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('display_name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        schema='public'
    )
    
    # ============================================================================
    # EXTEND EXISTING JURISDICTIONS TABLE
    # ============================================================================
    
    # Add government level tracking to existing jurisdictions table
    op.add_column('jurisdictions', sa.Column('level_id', sa.Integer(), nullable=True), schema='public')
    op.add_column('jurisdictions', sa.Column('short_name', sa.String(length=50), nullable=True), schema='public')
    op.add_column('jurisdictions', sa.Column('ocd_division_id', sa.String(length=200), nullable=True), schema='public')
    op.add_column('jurisdictions', sa.Column('census_code', sa.String(length=20), nullable=True), schema='public')
    op.add_column('jurisdictions', sa.Column('province_territory', sa.String(length=50), nullable=True), schema='public')
    
    # Add foreign key constraint to government_levels
    op.create_foreign_key(
        'fk_jurisdictions_government_levels', 'jurisdictions', 'government_levels',
        ['level_id'], ['id'], source_schema='public', referent_schema='public'
    )
    
    # ============================================================================
    # DATA PROVENANCE TRACKING (NEW - For legacy scraper integration)
    # ============================================================================
    
    # Create data_sources table to track all 136 legacy scrapers
    op.create_table('data_sources',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('url', sa.String(length=500), nullable=True),
        sa.Column('type', sa.String(length=100), nullable=True),
        sa.Column('jurisdiction_id', postgresql.UUID(as_uuid=True), nullable=True),  # Use UUID to match existing
        sa.Column('last_updated', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('metadata_json', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('legacy_module', sa.String(length=100), nullable=True),  # e.g., 'ca_on_toronto'
        sa.Column('legacy_class', sa.String(length=100), nullable=True),  # e.g., 'TorontoPersonScraper'
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['jurisdiction_id'], ['public.jurisdictions.id'], ),
        sa.PrimaryKeyConstraint('id'),
        schema='public'
    )
    
    # Create ingestion_logs table for monitoring data quality
    op.create_table('ingestion_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('data_source_id', sa.Integer(), nullable=False),
        sa.Column('operation', sa.String(length=100), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('records_processed', sa.Integer(), nullable=True),
        sa.Column('records_created', sa.Integer(), nullable=True),
        sa.Column('records_updated', sa.Integer(), nullable=True),
        sa.Column('records_failed', sa.Integer(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('duration_seconds', sa.Integer(), nullable=True),
        sa.Column('metadata_json', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['data_source_id'], ['public.data_sources.id'], ),
        sa.PrimaryKeyConstraint('id'),
        schema='public'
    )
    
    # ============================================================================
    # INDEXES FOR PERFORMANCE
    # ============================================================================
    
    # New indexes for extended jurisdictions table
    op.create_index('ix_jurisdictions_level_id', 'jurisdictions', ['level_id'], unique=False, schema='public')
    op.create_index('ix_jurisdictions_ocd_division_id', 'jurisdictions', ['ocd_division_id'], unique=False, schema='public')
    op.create_index('ix_jurisdictions_census_code', 'jurisdictions', ['census_code'], unique=False, schema='public')
    
    # Data sources indexes
    op.create_index('ix_data_sources_jurisdiction_id', 'data_sources', ['jurisdiction_id'], unique=False, schema='public')
    op.create_index('ix_data_sources_type', 'data_sources', ['type'], unique=False, schema='public')
    op.create_index('ix_data_sources_is_active', 'data_sources', ['is_active'], unique=False, schema='public')
    op.create_index('ix_data_sources_legacy_module', 'data_sources', ['legacy_module'], unique=False, schema='public')
    
    # Ingestion logs indexes
    op.create_index('ix_ingestion_logs_data_source_id', 'ingestion_logs', ['data_source_id'], unique=False, schema='public')
    op.create_index('ix_ingestion_logs_status', 'ingestion_logs', ['status'], unique=False, schema='public')
    op.create_index('ix_ingestion_logs_started_at', 'ingestion_logs', ['started_at'], unique=False, schema='public')
    op.create_index('ix_ingestion_logs_operation', 'ingestion_logs', ['operation'], unique=False, schema='public')

def downgrade() -> None:
    # Drop indexes first
    op.drop_index('ix_ingestion_logs_operation', table_name='ingestion_logs', schema='public')
    op.drop_index('ix_ingestion_logs_started_at', table_name='ingestion_logs', schema='public')
    op.drop_index('ix_ingestion_logs_status', table_name='ingestion_logs', schema='public')
    op.drop_index('ix_ingestion_logs_data_source_id', table_name='ingestion_logs', schema='public')
    
    op.drop_index('ix_data_sources_legacy_module', table_name='data_sources', schema='public')
    op.drop_index('ix_data_sources_is_active', table_name='data_sources', schema='public')
    op.drop_index('ix_data_sources_type', table_name='data_sources', schema='public')
    op.drop_index('ix_data_sources_jurisdiction_id', table_name='data_sources', schema='public')
    
    op.drop_index('ix_jurisdictions_census_code', table_name='jurisdictions', schema='public')
    op.drop_index('ix_jurisdictions_ocd_division_id', table_name='jurisdictions', schema='public')
    op.drop_index('ix_jurisdictions_level_id', table_name='jurisdictions', schema='public')
    
    # Drop tables in reverse order
    op.drop_table('ingestion_logs', schema='public')
    op.drop_table('data_sources', schema='public')
    
    # Remove added columns from existing jurisdictions table
    op.drop_column('jurisdictions', 'province_territory', schema='public')
    op.drop_column('jurisdictions', 'census_code', schema='public')
    op.drop_column('jurisdictions', 'ocd_division_id', schema='public')
    op.drop_column('jurisdictions', 'short_name', schema='public')
    
    # Drop foreign key constraint
    op.drop_constraint('fk_jurisdictions_government_levels', 'jurisdictions', schema='public')
    op.drop_column('jurisdictions', 'level_id', schema='public')
    
    # Drop government_levels table
    op.drop_table('government_levels', schema='public')

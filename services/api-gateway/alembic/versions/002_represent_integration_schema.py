"""Add Represent integration schema for legacy data

Revision ID: 002_represent_integration
Revises: 001_initial_schema
Create Date: 2025-08-20 18:50:00.000000

Following FUNDAMENTAL RULE: Schema designed to match legacy data structure
Source: services/etl/data/legacy_adapted/legacy_collected_20250820_182948.json
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002_represent_integration'
down_revision = '001_initial_schema'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # MP Offices table (following legacy data structure)
    op.create_table(
        'mp_offices',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('mp_id', sa.Integer(), sa.ForeignKey('members.id'), nullable=False),
        sa.Column('office_type', sa.String(50), nullable=False),  # 'legislature' or 'constituency'
        sa.Column('telephone', sa.String(50), nullable=True),
        sa.Column('fax', sa.String(50), nullable=True),
        sa.Column('postal_address', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # Add indexes for offices
    op.create_index('idx_mp_offices_mp_id', 'mp_offices', ['mp_id'])
    op.create_index('idx_mp_offices_type', 'mp_offices', ['office_type'])

    # Add new columns to members table for legacy data
    op.add_column('members', sa.Column('legacy_source', sa.String(50), nullable=True))  # 'represent_api' or 'ourcommons'
    op.add_column('members', sa.Column('extracted_at', sa.DateTime(), nullable=True))
    op.add_column('members', sa.Column('preferred_languages', postgresql.ARRAY(sa.String(50)), nullable=True))
    op.add_column('members', sa.Column('photo_url', sa.String(500), nullable=True))
    op.add_column('members', sa.Column('personal_url', sa.String(500), nullable=True))

    # Bills sponsors table (for bill sponsor relationships)
    op.create_table(
        'bill_sponsors',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('bill_id', sa.Integer(), sa.ForeignKey('bills.id'), nullable=False),
        sa.Column('member_id', sa.Integer(), sa.ForeignKey('members.id'), nullable=False),
        sa.Column('sponsor_type', sa.String(50), nullable=False),  # 'primary', 'secondary', etc.
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )

    # Add indexes for bill sponsors
    op.create_index('idx_bill_sponsors_bill_id', 'bill_sponsors', ['bill_id'])
    op.create_index('idx_bill_sponsors_member_id', 'bill_sponsors', ['member_id'])

    # Add new columns to bills table for legacy data
    op.add_column('bills', sa.Column('legisinfo_id', sa.String(50), nullable=True))
    op.add_column('bills', sa.Column('parliament_number', sa.Integer(), nullable=True))
    op.add_column('bills', sa.Column('session_number', sa.Integer(), nullable=True))
    op.add_column('bills', sa.Column('bill_type', sa.String(20), nullable=True))  # 'government', 'private', etc.
    op.add_column('bills', sa.Column('chamber', sa.String(20), nullable=True))  # 'house', 'senate'
    op.add_column('bills', sa.Column('sponsor_title', sa.String(200), nullable=True))
    op.add_column('bills', sa.Column('legacy_source', sa.String(50), nullable=True))
    op.add_column('bills', sa.Column('extracted_at', sa.DateTime(), nullable=True))

    # Vote ballots table (individual MP votes)
    op.create_table(
        'vote_ballots',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('vote_id', sa.Integer(), sa.ForeignKey('votes.id'), nullable=False),
        sa.Column('member_id', sa.Integer(), sa.ForeignKey('members.id'), nullable=False),
        sa.Column('ballot', sa.String(20), nullable=False),  # 'Yea', 'Nay', 'Paired'
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )

    # Add indexes for vote ballots
    op.create_index('idx_vote_ballots_vote_id', 'vote_ballots', ['vote_id'])
    op.create_index('idx_vote_ballots_member_id', 'vote_ballots', ['member_id'])
    op.create_index('idx_vote_ballots_ballot', 'vote_ballots', ['ballot'])

    # Add new columns to votes table for legacy data
    op.add_column('votes', sa.Column('parliament_number', sa.Integer(), nullable=True))
    op.add_column('votes', sa.Column('session_number', sa.Integer(), nullable=True))
    op.add_column('votes', sa.Column('vote_number', sa.Integer(), nullable=True))
    op.add_column('votes', sa.Column('vote_type', sa.String(50), nullable=True))
    op.add_column('votes', sa.Column('result', sa.String(20), nullable=True))  # 'Agreed to', 'Negatived'
    op.add_column('votes', sa.Column('yea_count', sa.Integer(), nullable=True))
    op.add_column('votes', sa.Column('nay_count', sa.Integer(), nullable=True))
    op.add_column('votes', sa.Column('paired_count', sa.Integer(), nullable=True))
    op.add_column('votes', sa.Column('legacy_source', sa.String(50), nullable=True))
    op.add_column('votes', sa.Column('extracted_at', sa.DateTime(), nullable=True))

    # Electoral districts table (for Represent data)
    op.create_table(
        'electoral_districts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('boundary_set_name', sa.String(200), nullable=False),
        sa.Column('external_id', sa.String(100), nullable=True),
        sa.Column('centroid_lat', sa.Float(), nullable=True),
        sa.Column('centroid_lon', sa.Float(), nullable=True),
        sa.Column('area_km2', sa.Float(), nullable=True),
        sa.Column('province', sa.String(2), nullable=True),  # AB, BC, etc.
        sa.Column('level', sa.String(20), nullable=False),  # 'federal', 'provincial', 'municipal'
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # Add indexes for electoral districts
    op.create_index('idx_electoral_districts_name', 'electoral_districts', ['name'])
    op.create_index('idx_electoral_districts_level', 'electoral_districts', ['level'])
    op.create_index('idx_electoral_districts_province', 'electoral_districts', ['province'])

    # Data collection runs table (to track legacy imports)
    op.create_table(
        'data_collection_runs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('run_type', sa.String(50), nullable=False),  # 'legacy_full', 'legacy_incremental'
        sa.Column('started_at', sa.DateTime(), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(20), nullable=False),  # 'running', 'completed', 'failed'
        sa.Column('mps_collected', sa.Integer(), nullable=True),
        sa.Column('bills_collected', sa.Integer(), nullable=True),
        sa.Column('votes_collected', sa.Integer(), nullable=True),
        sa.Column('source_file', sa.String(500), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )

    # Add indexes for data collection runs
    op.create_index('idx_data_collection_runs_status', 'data_collection_runs', ['status'])
    op.create_index('idx_data_collection_runs_started_at', 'data_collection_runs', ['started_at'])


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('data_collection_runs')
    op.drop_table('electoral_districts')
    op.drop_table('vote_ballots')
    op.drop_table('bill_sponsors')
    op.drop_table('mp_offices')
    
    # Remove added columns from existing tables
    op.drop_column('votes', 'extracted_at')
    op.drop_column('votes', 'legacy_source')
    op.drop_column('votes', 'paired_count')
    op.drop_column('votes', 'nay_count')
    op.drop_column('votes', 'yea_count')
    op.drop_column('votes', 'result')
    op.drop_column('votes', 'vote_type')
    op.drop_column('votes', 'vote_number')
    op.drop_column('votes', 'session_number')
    op.drop_column('votes', 'parliament_number')
    
    op.drop_column('bills', 'extracted_at')
    op.drop_column('bills', 'legacy_source')
    op.drop_column('bills', 'sponsor_title')
    op.drop_column('bills', 'chamber')
    op.drop_column('bills', 'bill_type')
    op.drop_column('bills', 'session_number')
    op.drop_column('bills', 'parliament_number')
    op.drop_column('bills', 'legisinfo_id')
    
    op.drop_column('members', 'personal_url')
    op.drop_column('members', 'photo_url')
    op.drop_column('members', 'preferred_languages')
    op.drop_column('members', 'extracted_at')
    op.drop_column('members', 'legacy_source')

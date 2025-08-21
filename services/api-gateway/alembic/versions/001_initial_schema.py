"""Initial schema for OpenParliament.ca V2

Revision ID: 001_initial_schema
Revises: 
Create Date: 2025-08-20 19:00:00.000000

Following FUNDAMENTAL RULE: Schema designed to match legacy data structure
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Members table (MPs)
    op.create_table(
        'members',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('party', sa.String(100), nullable=True),
        sa.Column('riding', sa.String(200), nullable=True),
        sa.Column('province', sa.String(50), nullable=True),
        sa.Column('email', sa.String(200), nullable=True),
        sa.Column('website', sa.String(500), nullable=True),
        sa.Column('twitter', sa.String(100), nullable=True),
        sa.Column('facebook', sa.String(100), nullable=True),
        sa.Column('instagram', sa.String(100), nullable=True),
        sa.Column('youtube', sa.String(100), nullable=True),
        sa.Column('linkedin', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # Bills table
    op.create_table(
        'bills',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('number', sa.String(50), nullable=False),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('status', sa.String(100), nullable=True),
        sa.Column('introduced_date', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # Votes table
    op.create_table(
        'votes',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('bill_id', sa.Integer(), sa.ForeignKey('bills.id'), nullable=True),
        sa.Column('question', sa.String(500), nullable=False),
        sa.Column('date', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # Data collection runs table
    op.create_table(
        'data_collection_runs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('run_date', sa.DateTime(), nullable=False),
        sa.Column('source', sa.String(100), nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('records_collected', sa.Integer(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )

    # Add indexes
    op.create_index('idx_members_party', 'members', ['party'])
    op.create_index('idx_members_riding', 'members', ['riding'])
    op.create_index('idx_members_province', 'members', ['province'])
    op.create_index('idx_bills_number', 'bills', ['number'])
    op.create_index('idx_bills_status', 'bills', ['status'])
    op.create_index('idx_votes_bill_id', 'votes', ['bill_id'])
    op.create_index('idx_votes_date', 'votes', ['date'])


def downgrade() -> None:
    op.drop_table('data_collection_runs')
    op.drop_table('votes')
    op.drop_table('bills')
    op.drop_table('members')

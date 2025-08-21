"""Add municipal tables for legacy scrapers

Revision ID: 003
Revises: 002_represent_integration
Create Date: 2025-01-27 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002_represent_integration'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add municipal tables for legacy scrapers."""
    
    # Create municipalities table
    op.create_table('municipalities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('division_id', sa.String(length=100), nullable=True),
        sa.Column('division_name', sa.String(length=200), nullable=True),
        sa.Column('classification', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        schema='public'
    )
    
    # Create municipal_councillors table
    op.create_table('municipal_councillors',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('municipality', sa.String(length=100), nullable=False),
        sa.Column('municipality_name', sa.String(length=200), nullable=True),
        sa.Column('division_id', sa.String(length=100), nullable=True),
        sa.Column('division_name', sa.String(length=200), nullable=True),
        sa.Column('classification', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['municipality'], ['public.municipalities.name'], ),
        sa.PrimaryKeyConstraint('id'),
        schema='public'
    )
    
    # Create municipal_offices table
    op.create_table('municipal_offices',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('councillor_id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('value', sa.String(length=500), nullable=False),
        sa.Column('note', sa.String(length=100), nullable=True),
        sa.Column('label', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['councillor_id'], ['public.municipal_councillors.id'], ),
        sa.PrimaryKeyConstraint('id'),
        schema='public'
    )
    
    # Create indexes for better performance
    op.create_index('ix_public_municipal_councillors_municipality', 'municipal_councillors', ['municipality'], unique=False, schema='public')
    op.create_index('ix_public_municipal_offices_councillor_id', 'municipal_offices', ['councillor_id'], unique=False, schema='public')
    op.create_index('ix_public_municipal_offices_type', 'municipal_offices', ['type'], unique=False, schema='public')


def downgrade() -> None:
    """Remove municipal tables."""
    
    # Drop indexes
    op.drop_index('ix_public_municipal_offices_type', table_name='municipal_offices', schema='public')
    op.drop_index('ix_public_municipal_offices_councillor_id', table_name='municipal_offices', schema='public')
    op.drop_index('ix_public_municipal_councillors_municipality', table_name='municipal_councillors', schema='public')
    
    # Drop tables
    op.drop_table('municipal_offices', schema='public')
    op.drop_table('municipal_councillors', schema='public')
    op.drop_table('municipalities', schema='public')

"""Create feature flags system

Revision ID: 006_feature_flags_system
Revises: 005
Create Date: 2025-08-23 17:15:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '006_feature_flags_system'
down_revision = '005'
branch_labels = None
depends_on = None


def upgrade():
    # Rename pwa_features table to feature_flags
    op.rename_table('pwa_features', 'feature_flags')
    
    # Add new columns to feature_flags table
    op.add_column('feature_flags', sa.Column('flag_type', sa.String(50), server_default='feature', nullable=True))
    op.add_column('feature_flags', sa.Column('targeting_rules', postgresql.JSONB(), nullable=True))
    op.add_column('feature_flags', sa.Column('rollout_percentage', sa.Integer(), server_default='0', nullable=True))
    op.add_column('feature_flags', sa.Column('environments', postgresql.JSONB(), server_default='["all"]', nullable=True))
    op.add_column('feature_flags', sa.Column('user_overrides', postgresql.JSONB(), nullable=True))
    op.add_column('feature_flags', sa.Column('start_date', sa.DateTime(), nullable=True))
    op.add_column('feature_flags', sa.Column('end_date', sa.DateTime(), nullable=True))
    op.add_column('feature_flags', sa.Column('dependencies', postgresql.JSONB(), nullable=True))
    
    # Update constraints
    op.drop_constraint('uq_pwa_feature_manifest_name', 'feature_flags', type_='unique')
    op.create_unique_constraint('uq_feature_flag_name', 'feature_flags', ['feature_name'])
    
    # Make manifest_id nullable since not all feature flags need PWA manifest
    op.alter_column('feature_flags', 'manifest_id',
                    existing_type=postgresql.UUID(),
                    nullable=True)
    
    # Create feature_evaluations table
    op.create_table('feature_evaluations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('flag_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', sa.String(255), nullable=True),
        sa.Column('evaluation_result', sa.Boolean(), nullable=False),
        sa.Column('evaluation_context', postgresql.JSONB(), nullable=True),
        sa.Column('evaluated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['flag_id'], ['feature_flags.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_feature_evaluations_flag_id', 'feature_evaluations', ['flag_id'])
    op.create_index('ix_feature_evaluations_user_id', 'feature_evaluations', ['user_id'])
    op.create_index('ix_feature_evaluations_evaluated_at', 'feature_evaluations', ['evaluated_at'])
    
    # Create feature_flag_changes audit table
    op.create_table('feature_flag_changes',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('flag_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('changed_by', sa.String(255), nullable=False),
        sa.Column('change_type', sa.String(50), nullable=False),
        sa.Column('old_value', postgresql.JSONB(), nullable=True),
        sa.Column('new_value', postgresql.JSONB(), nullable=True),
        sa.Column('changed_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['flag_id'], ['feature_flags.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_feature_flag_changes_flag_id', 'feature_flag_changes', ['flag_id'])
    op.create_index('ix_feature_flag_changes_changed_by', 'feature_flag_changes', ['changed_by'])
    op.create_index('ix_feature_flag_changes_changed_at', 'feature_flag_changes', ['changed_at'])
    
    # Add new indexes to feature_flags
    op.create_index('ix_feature_flags_flag_type', 'feature_flags', ['flag_type'])
    op.create_index('ix_feature_flags_rollout_percentage', 'feature_flags', ['rollout_percentage'])
    op.create_index('ix_feature_flags_start_date', 'feature_flags', ['start_date'])
    op.create_index('ix_feature_flags_end_date', 'feature_flags', ['end_date'])


def downgrade():
    # Drop new indexes
    op.drop_index('ix_feature_flags_end_date', table_name='feature_flags')
    op.drop_index('ix_feature_flags_start_date', table_name='feature_flags')
    op.drop_index('ix_feature_flags_rollout_percentage', table_name='feature_flags')
    op.drop_index('ix_feature_flags_flag_type', table_name='feature_flags')
    
    # Drop audit tables
    op.drop_table('feature_flag_changes')
    op.drop_table('feature_evaluations')
    
    # Restore original constraint
    op.drop_constraint('uq_feature_flag_name', 'feature_flags', type_='unique')
    op.create_unique_constraint('uq_pwa_feature_manifest_name', 'feature_flags', ['manifest_id', 'feature_name'])
    
    # Make manifest_id not nullable again
    op.alter_column('feature_flags', 'manifest_id',
                    existing_type=postgresql.UUID(),
                    nullable=False)
    
    # Drop new columns
    op.drop_column('feature_flags', 'dependencies')
    op.drop_column('feature_flags', 'end_date')
    op.drop_column('feature_flags', 'start_date')
    op.drop_column('feature_flags', 'user_overrides')
    op.drop_column('feature_flags', 'environments')
    op.drop_column('feature_flags', 'rollout_percentage')
    op.drop_column('feature_flags', 'targeting_rules')
    op.drop_column('feature_flags', 'flag_type')
    
    # Rename table back
    op.rename_table('feature_flags', 'pwa_features')
"""
Data Dashboard System

Revision ID: 011_data_dashboard_system
Revises: 010_debate_transcript_system
Create Date: 2025-08-23 23:00:00

Implements FEAT-005 Data Dashboard (P2 priority).
Creates tables for enhanced dashboard and analytics system.
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '011_data_dashboard_system'
down_revision = '010_debate_transcript_system'
branch_labels = None
depends_on = None


def upgrade():
    """Create data dashboard tables."""
    
    # Create dashboard_templates table
    op.create_table(
        'dashboard_templates',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('slug', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('type', sa.Enum('overview', 'analytics', 'performance', 'legislative', 'member', 'bill', 'committee', 'custom', name='dashboardtype'), nullable=False),
        sa.Column('is_public', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('is_default', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('requires_auth', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('layout_config', postgresql.JSONB(), nullable=False),
        sa.Column('widget_configs', postgresql.JSONB(), nullable=False),
        sa.Column('tags', postgresql.JSONB(), nullable=True),
        sa.Column('category', sa.String(100), nullable=True),
        sa.Column('icon', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.UniqueConstraint('slug')
    )
    
    # Create indexes for dashboard_templates
    op.create_index('idx_template_slug', 'dashboard_templates', ['slug'])
    op.create_index('idx_template_type', 'dashboard_templates', ['type'])
    op.create_index('idx_template_public', 'dashboard_templates', ['is_public'])
    
    # Create user_dashboards table
    op.create_table(
        'user_dashboards',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('template_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('slug', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('type', sa.Enum('overview', 'analytics', 'performance', 'legislative', 'member', 'bill', 'committee', 'custom', name='dashboardtype'), nullable=False),
        sa.Column('layout_config', postgresql.JSONB(), nullable=False),
        sa.Column('theme', postgresql.JSONB(), nullable=True),
        sa.Column('is_public', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('is_favorite', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('refresh_interval', sa.Enum('real_time', '1m', '5m', '15m', '1h', '6h', 'daily', 'manual', name='refreshinterval'), server_default='5m', nullable=False),
        sa.Column('share_token', sa.String(100), nullable=True),
        sa.Column('share_expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=True),
        sa.Column('last_accessed_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['template_id'], ['dashboard_templates.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('share_token')
    )
    
    # Create indexes for user_dashboards
    op.create_index('idx_dashboard_user', 'user_dashboards', ['user_id'])
    op.create_index('idx_dashboard_slug', 'user_dashboards', ['user_id', 'slug'], unique=True)
    op.create_index('idx_dashboard_favorite', 'user_dashboards', ['user_id', 'is_favorite'])
    op.create_index('idx_dashboard_share_token', 'user_dashboards', ['share_token'])
    
    # Create dashboard_widgets table
    op.create_table(
        'dashboard_widgets',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('dashboard_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('widget_type', sa.Enum('chart', 'metric', 'table', 'map', 'timeline', 'activity_feed', 'comparison', 'heatmap', name='widgettype'), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('subtitle', sa.String(500), nullable=True),
        sa.Column('data_source', sa.String(100), nullable=False),
        sa.Column('data_query', postgresql.JSONB(), nullable=False),
        sa.Column('data_filters', postgresql.JSONB(), nullable=True),
        sa.Column('display_config', postgresql.JSONB(), nullable=False),
        sa.Column('position', postgresql.JSONB(), nullable=False),
        sa.Column('is_interactive', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('click_action', postgresql.JSONB(), nullable=True),
        sa.Column('drill_down_config', postgresql.JSONB(), nullable=True),
        sa.Column('cache_duration', sa.Integer(), nullable=True),
        sa.Column('last_refresh', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['dashboard_id'], ['user_dashboards.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for dashboard_widgets
    op.create_index('idx_widget_dashboard', 'dashboard_widgets', ['dashboard_id'])
    op.create_index('idx_widget_type', 'dashboard_widgets', ['widget_type'])
    
    # Create widget_metrics table
    op.create_table(
        'widget_metrics',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('widget_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('metric_key', sa.String(100), nullable=False),
        sa.Column('metric_label', sa.String(200), nullable=False),
        sa.Column('metric_value', postgresql.JSONB(), nullable=False),
        sa.Column('previous_value', postgresql.JSONB(), nullable=True),
        sa.Column('change_percentage', postgresql.JSONB(), nullable=True),
        sa.Column('trend_direction', sa.String(20), nullable=True),
        sa.Column('format_type', sa.String(50), nullable=True),
        sa.Column('unit', sa.String(50), nullable=True),
        sa.Column('icon', sa.String(100), nullable=True),
        sa.Column('color', sa.String(50), nullable=True),
        sa.Column('calculated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['widget_id'], ['dashboard_widgets.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for widget_metrics
    op.create_index('idx_metric_widget', 'widget_metrics', ['widget_id'])
    op.create_index('idx_metric_key', 'widget_metrics', ['metric_key'])
    
    # Create dashboard_alerts table
    op.create_table(
        'dashboard_alerts',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('dashboard_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('widget_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('condition', postgresql.JSONB(), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('notification_channels', postgresql.JSONB(), nullable=False),
        sa.Column('check_interval', sa.Enum('real_time', '1m', '5m', '15m', '1h', '6h', 'daily', 'manual', name='refreshinterval'), server_default='15m', nullable=False),
        sa.Column('last_checked', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_triggered', sa.DateTime(timezone=True), nullable=True),
        sa.Column('trigger_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['dashboard_id'], ['user_dashboards.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['widget_id'], ['dashboard_widgets.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for dashboard_alerts
    op.create_index('idx_alert_user', 'dashboard_alerts', ['user_id'])
    op.create_index('idx_alert_active', 'dashboard_alerts', ['is_active'])
    op.create_index('idx_alert_check', 'dashboard_alerts', ['is_active', 'check_interval'])
    
    # Create data_queries table
    op.create_table(
        'data_queries',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('query_type', sa.String(50), nullable=False),
        sa.Column('query_config', postgresql.JSONB(), nullable=False),
        sa.Column('parameters', postgresql.JSONB(), nullable=True),
        sa.Column('is_public', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('is_system', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('required_permissions', postgresql.JSONB(), nullable=True),
        sa.Column('estimated_cost', sa.Integer(), nullable=True),
        sa.Column('timeout_seconds', sa.Integer(), server_default='30', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=True),
        sa.Column('last_executed', sa.DateTime(timezone=True), nullable=True),
        sa.Column('execution_count', sa.Integer(), server_default='0', nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # Create indexes for data_queries
    op.create_index('idx_query_name', 'data_queries', ['name'])
    op.create_index('idx_query_type', 'data_queries', ['query_type'])
    op.create_index('idx_query_public', 'data_queries', ['is_public'])
    
    # Create dashboard_snapshots table
    op.create_table(
        'dashboard_snapshots',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('dashboard_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('dashboard_state', postgresql.JSONB(), nullable=False),
        sa.Column('widget_data', postgresql.JSONB(), nullable=False),
        sa.Column('is_public', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('share_token', sa.String(100), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('tags', postgresql.JSONB(), nullable=True),
        sa.Column('view_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['dashboard_id'], ['user_dashboards.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('share_token')
    )
    
    # Create indexes for dashboard_snapshots
    op.create_index('idx_snapshot_dashboard', 'dashboard_snapshots', ['dashboard_id'])
    op.create_index('idx_snapshot_user', 'dashboard_snapshots', ['user_id'])
    op.create_index('idx_snapshot_public', 'dashboard_snapshots', ['is_public'])
    op.create_index('idx_snapshot_token', 'dashboard_snapshots', ['share_token'])
    
    # Insert default templates
    from sqlalchemy.sql import table, column
    import uuid
    
    templates_table = table(
        'dashboard_templates',
        column('id', postgresql.UUID),
        column('name', sa.String),
        column('slug', sa.String),
        column('description', sa.Text),
        column('type', sa.String),
        column('is_public', sa.Boolean),
        column('is_default', sa.Boolean),
        column('layout_config', postgresql.JSONB),
        column('widget_configs', postgresql.JSONB),
        column('category', sa.String),
        column('icon', sa.String)
    )
    
    default_templates = [
        {
            'id': uuid.uuid4(),
            'name': 'Legislative Overview',
            'slug': 'legislative-overview',
            'description': 'Overview of legislative activity including bills, votes, and committee work',
            'type': 'legislative',
            'is_public': True,
            'is_default': True,
            'layout_config': {
                'rows': 12,
                'cols': 12,
                'rowHeight': 80,
                'margin': [10, 10]
            },
            'widget_configs': [
                {
                    'widget_type': 'metric',
                    'title': 'Active Bills',
                    'data_source': '/api/v1/bills/stats',
                    'data_query': {'status': 'active'},
                    'display_config': {'format': 'number', 'icon': 'file-text'},
                    'position': {'x': 0, 'y': 0, 'w': 3, 'h': 2}
                },
                {
                    'widget_type': 'metric',
                    'title': 'Recent Votes',
                    'data_source': '/api/v1/votes/stats',
                    'data_query': {'days': 7},
                    'display_config': {'format': 'number', 'icon': 'check-square'},
                    'position': {'x': 3, 'y': 0, 'w': 3, 'h': 2}
                },
                {
                    'widget_type': 'chart',
                    'title': 'Bill Progress by Stage',
                    'data_source': '/api/v1/bills/progress',
                    'data_query': {},
                    'display_config': {'chartType': 'bar'},
                    'position': {'x': 6, 'y': 0, 'w': 6, 'h': 4}
                },
                {
                    'widget_type': 'table',
                    'title': 'Recent Legislative Activity',
                    'data_source': '/api/v1/activities/recent',
                    'data_query': {'limit': 10},
                    'display_config': {'columns': ['date', 'type', 'title', 'status']},
                    'position': {'x': 0, 'y': 4, 'w': 12, 'h': 6}
                }
            ],
            'category': 'government',
            'icon': 'parliament'
        },
        {
            'id': uuid.uuid4(),
            'name': 'Member Performance Dashboard',
            'slug': 'member-performance',
            'description': 'Track member activity, voting patterns, and engagement',
            'type': 'member',
            'is_public': True,
            'is_default': True,
            'layout_config': {
                'rows': 12,
                'cols': 12,
                'rowHeight': 80,
                'margin': [10, 10]
            },
            'widget_configs': [
                {
                    'widget_type': 'metric',
                    'title': 'Attendance Rate',
                    'data_source': '/api/v1/members/stats/attendance',
                    'data_query': {},
                    'display_config': {'format': 'percentage', 'icon': 'user-check'},
                    'position': {'x': 0, 'y': 0, 'w': 4, 'h': 2}
                },
                {
                    'widget_type': 'chart',
                    'title': 'Voting Participation',
                    'data_source': '/api/v1/members/stats/voting',
                    'data_query': {'period': 'monthly'},
                    'display_config': {'chartType': 'line'},
                    'position': {'x': 4, 'y': 0, 'w': 8, 'h': 4}
                },
                {
                    'widget_type': 'heatmap',
                    'title': 'Committee Participation',
                    'data_source': '/api/v1/members/stats/committees',
                    'data_query': {},
                    'display_config': {},
                    'position': {'x': 0, 'y': 4, 'w': 6, 'h': 4}
                }
            ],
            'category': 'analytics',
            'icon': 'users'
        },
        {
            'id': uuid.uuid4(),
            'name': 'System Performance',
            'slug': 'system-performance',
            'description': 'Monitor system health, API performance, and data quality',
            'type': 'performance',
            'is_public': False,
            'is_default': True,
            'layout_config': {
                'rows': 12,
                'cols': 12,
                'rowHeight': 80,
                'margin': [10, 10]
            },
            'widget_configs': [
                {
                    'widget_type': 'metric',
                    'title': 'API Response Time',
                    'data_source': '/api/v1/performance/response-time',
                    'data_query': {'metric': 'p95'},
                    'display_config': {'format': 'duration', 'unit': 'ms', 'icon': 'activity'},
                    'position': {'x': 0, 'y': 0, 'w': 3, 'h': 2}
                },
                {
                    'widget_type': 'metric',
                    'title': 'Data Quality Score',
                    'data_source': '/api/v1/performance/quality',
                    'data_query': {},
                    'display_config': {'format': 'percentage', 'icon': 'shield'},
                    'position': {'x': 3, 'y': 0, 'w': 3, 'h': 2}
                },
                {
                    'widget_type': 'timeline',
                    'title': 'System Events',
                    'data_source': '/api/v1/performance/events',
                    'data_query': {'hours': 24},
                    'display_config': {},
                    'position': {'x': 0, 'y': 2, 'w': 12, 'h': 4}
                }
            ],
            'category': 'system',
            'icon': 'monitor'
        }
    ]
    
    op.bulk_insert(templates_table, default_templates)


def downgrade():
    """Drop data dashboard tables."""
    
    # Drop tables in reverse order due to foreign key constraints
    op.drop_index('idx_snapshot_token', table_name='dashboard_snapshots')
    op.drop_index('idx_snapshot_public', table_name='dashboard_snapshots')
    op.drop_index('idx_snapshot_user', table_name='dashboard_snapshots')
    op.drop_index('idx_snapshot_dashboard', table_name='dashboard_snapshots')
    op.drop_table('dashboard_snapshots')
    
    op.drop_index('idx_query_public', table_name='data_queries')
    op.drop_index('idx_query_type', table_name='data_queries')
    op.drop_index('idx_query_name', table_name='data_queries')
    op.drop_table('data_queries')
    
    op.drop_index('idx_alert_check', table_name='dashboard_alerts')
    op.drop_index('idx_alert_active', table_name='dashboard_alerts')
    op.drop_index('idx_alert_user', table_name='dashboard_alerts')
    op.drop_table('dashboard_alerts')
    
    op.drop_index('idx_metric_key', table_name='widget_metrics')
    op.drop_index('idx_metric_widget', table_name='widget_metrics')
    op.drop_table('widget_metrics')
    
    op.drop_index('idx_widget_type', table_name='dashboard_widgets')
    op.drop_index('idx_widget_dashboard', table_name='dashboard_widgets')
    op.drop_table('dashboard_widgets')
    
    op.drop_index('idx_dashboard_share_token', table_name='user_dashboards')
    op.drop_index('idx_dashboard_favorite', table_name='user_dashboards')
    op.drop_index('idx_dashboard_slug', table_name='user_dashboards')
    op.drop_index('idx_dashboard_user', table_name='user_dashboards')
    op.drop_table('user_dashboards')
    
    op.drop_index('idx_template_public', table_name='dashboard_templates')
    op.drop_index('idx_template_type', table_name='dashboard_templates')
    op.drop_index('idx_template_slug', table_name='dashboard_templates')
    op.drop_table('dashboard_templates')
    
    # Drop enums
    op.execute('DROP TYPE IF EXISTS dashboardtype')
    op.execute('DROP TYPE IF EXISTS widgettype')
    op.execute('DROP TYPE IF EXISTS refreshinterval')
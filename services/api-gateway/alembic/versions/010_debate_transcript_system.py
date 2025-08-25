"""
Debate Transcript System

Revision ID: 010_debate_transcript_system
Revises: 009_feedback_collection_system
Create Date: 2025-08-23 22:00:00

Implements FEAT-018 Debate Transcripts (P1 priority).
Creates tables for parliamentary debate transcript management.
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '010_debate_transcript_system'
down_revision = '009_feedback_collection_system'
branch_labels = None
depends_on = None


def upgrade():
    """Create debate transcript tables."""
    
    # Create debate_sessions table
    op.create_table(
        'debate_sessions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('parliament_number', sa.Integer(), nullable=False),
        sa.Column('session_number', sa.Integer(), nullable=False),
        sa.Column('sitting_number', sa.Integer(), nullable=False),
        sa.Column('sitting_date', sa.Date(), nullable=False),
        sa.Column('document_number', sa.String(50), nullable=False),
        sa.Column('source_url', sa.String(500), nullable=True),
        sa.Column('language', sa.String(10), server_default='en', nullable=False),
        sa.Column('is_bilingual', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('start_time', sa.Time(), nullable=True),
        sa.Column('end_time', sa.Time(), nullable=True),
        sa.Column('house_status', sa.String(50), nullable=True),
        sa.Column('total_statements', sa.Integer(), server_default='0', nullable=False),
        sa.Column('total_words', sa.Integer(), server_default='0', nullable=False),
        sa.Column('total_speakers', sa.Integer(), server_default='0', nullable=False),
        sa.Column('topics', postgresql.JSONB(), nullable=True),
        sa.Column('bills_discussed', postgresql.JSONB(), nullable=True),
        sa.Column('committees_mentioned', postgresql.JSONB(), nullable=True),
        sa.Column('search_vector', postgresql.TSVECTOR(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('document_number')
    )
    
    # Create indexes for debate_sessions
    op.create_index('idx_debate_session_date', 'debate_sessions', ['sitting_date'])
    op.create_index('idx_debate_session_parliament', 'debate_sessions', ['parliament_number', 'session_number'])
    op.create_index('idx_debate_session_number', 'debate_sessions', ['document_number'])
    op.create_index('idx_debate_session_search', 'debate_sessions', ['search_vector'], postgresql_using='gin')
    
    # Create debate_speakers table
    op.create_table(
        'debate_speakers',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('normalized_name', sa.String(200), nullable=False),
        sa.Column('member_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('party', sa.String(100), nullable=True),
        sa.Column('riding', sa.String(200), nullable=True),
        sa.Column('province', sa.String(50), nullable=True),
        sa.Column('role', sa.String(100), nullable=True),
        sa.Column('total_statements', sa.Integer(), server_default='0', nullable=False),
        sa.Column('total_words', sa.Integer(), server_default='0', nullable=False),
        sa.Column('first_seen', sa.Date(), nullable=True),
        sa.Column('last_seen', sa.Date(), nullable=True),
        sa.Column('alternate_names', postgresql.JSONB(), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['member_id'], ['openpolicy.members.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for debate_speakers
    op.create_index('idx_speaker_name', 'debate_speakers', ['normalized_name'])
    op.create_index('idx_speaker_member', 'debate_speakers', ['member_id'])
    op.create_index('idx_speaker_party', 'debate_speakers', ['party'])
    
    # Create debate_statements table
    op.create_table(
        'debate_statements',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('session_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('sequence_number', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.Time(), nullable=True),
        sa.Column('statement_type', sa.String(50), nullable=False),
        sa.Column('speaker_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('speaker_role', sa.String(100), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('content_fr', sa.Text(), nullable=True),
        sa.Column('language', sa.String(10), server_default='en', nullable=False),
        sa.Column('word_count', sa.Integer(), nullable=False),
        sa.Column('topic', sa.String(200), nullable=True),
        sa.Column('bill_reference', sa.String(50), nullable=True),
        sa.Column('references', postgresql.JSONB(), nullable=True),
        sa.Column('interjections', postgresql.JSONB(), nullable=True),
        sa.Column('search_vector', postgresql.TSVECTOR(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['session_id'], ['debate_sessions.id'], ),
        sa.ForeignKeyConstraint(['speaker_id'], ['debate_speakers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for debate_statements
    op.create_index('idx_statement_session', 'debate_statements', ['session_id'])
    op.create_index('idx_statement_speaker', 'debate_statements', ['speaker_id'])
    op.create_index('idx_statement_sequence', 'debate_statements', ['session_id', 'sequence_number'])
    op.create_index('idx_statement_type', 'debate_statements', ['statement_type'])
    op.create_index('idx_statement_search', 'debate_statements', ['search_vector'], postgresql_using='gin')
    
    # Create debate_session_speakers association table
    op.create_table(
        'debate_session_speakers',
        sa.Column('session_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('speaker_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('statement_count', sa.Integer(), server_default='0', nullable=True),
        sa.Column('word_count', sa.Integer(), server_default='0', nullable=True),
        sa.ForeignKeyConstraint(['session_id'], ['debate_sessions.id'], ),
        sa.ForeignKeyConstraint(['speaker_id'], ['debate_speakers.id'], ),
        sa.PrimaryKeyConstraint('session_id', 'speaker_id')
    )
    
    # Create debate_annotations table
    op.create_table(
        'debate_annotations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('statement_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('annotation_type', sa.String(50), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('is_official', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['statement_id'], ['debate_statements.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for debate_annotations
    op.create_index('idx_annotation_statement', 'debate_annotations', ['statement_id'])
    op.create_index('idx_annotation_type', 'debate_annotations', ['annotation_type'])
    
    # Create debate_searches table
    op.create_table(
        'debate_searches',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('query', sa.Text(), nullable=False),
        sa.Column('filters', postgresql.JSONB(), nullable=False),
        sa.Column('is_public', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('email_alerts', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('run_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('last_run', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for debate_searches
    op.create_index('idx_search_user', 'debate_searches', ['user_id'])
    op.create_index('idx_search_public', 'debate_searches', ['is_public'])
    
    # Create debate_topics table
    op.create_table(
        'debate_topics',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('slug', sa.String(200), nullable=False),
        sa.Column('category', sa.String(100), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('keywords', postgresql.JSONB(), nullable=True),
        sa.Column('mention_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('first_mentioned', sa.Date(), nullable=True),
        sa.Column('last_mentioned', sa.Date(), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('auto_detected', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.UniqueConstraint('slug')
    )
    
    # Create indexes for debate_topics
    op.create_index('idx_topic_slug', 'debate_topics', ['slug'])
    op.create_index('idx_topic_category', 'debate_topics', ['category'])
    
    # Create debate_analytics table
    op.create_table(
        'debate_analytics',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('session_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('top_words', postgresql.JSONB(), nullable=True),
        sa.Column('word_cloud_data', postgresql.JSONB(), nullable=True),
        sa.Column('topic_distribution', postgresql.JSONB(), nullable=True),
        sa.Column('sentiment_scores', postgresql.JSONB(), nullable=True),
        sa.Column('speaker_time_distribution', postgresql.JSONB(), nullable=True),
        sa.Column('party_participation', postgresql.JSONB(), nullable=True),
        sa.Column('interruption_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('question_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('auto_summary', sa.Text(), nullable=True),
        sa.Column('key_points', postgresql.JSONB(), nullable=True),
        sa.Column('computed_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('computation_time_ms', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['session_id'], ['debate_sessions.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('session_id')
    )
    
    # Create index for debate_analytics
    op.create_index('idx_analytics_session', 'debate_analytics', ['session_id'])
    
    # Insert default topics
    from sqlalchemy.sql import table, column
    import uuid
    
    topics_table = table(
        'debate_topics',
        column('id', postgresql.UUID),
        column('name', sa.String),
        column('slug', sa.String),
        column('category', sa.String),
        column('description', sa.Text)
    )
    
    default_topics = [
        {
            'id': uuid.uuid4(),
            'name': 'Budget and Finance',
            'slug': 'budget-and-finance',
            'category': 'economy',
            'description': 'Discussions related to federal budget, fiscal policy, and government spending'
        },
        {
            'id': uuid.uuid4(),
            'name': 'Healthcare',
            'slug': 'healthcare',
            'category': 'social',
            'description': 'Healthcare policy, medical services, and public health matters'
        },
        {
            'id': uuid.uuid4(),
            'name': 'Climate Change',
            'slug': 'climate-change',
            'category': 'environment',
            'description': 'Climate change policy, environmental protection, and sustainability'
        },
        {
            'id': uuid.uuid4(),
            'name': 'National Security',
            'slug': 'national-security',
            'category': 'security',
            'description': 'National defense, security policy, and public safety'
        },
        {
            'id': uuid.uuid4(),
            'name': 'Indigenous Affairs',
            'slug': 'indigenous-affairs',
            'category': 'social',
            'description': 'Indigenous rights, reconciliation, and First Nations policy'
        },
        {
            'id': uuid.uuid4(),
            'name': 'International Trade',
            'slug': 'international-trade',
            'category': 'economy',
            'description': 'Trade agreements, international commerce, and export/import policy'
        }
    ]
    
    op.bulk_insert(topics_table, default_topics)
    
    # Create trigger for updating search vectors
    op.execute("""
        CREATE OR REPLACE FUNCTION update_debate_search_vector() RETURNS trigger AS $$
        BEGIN
            NEW.search_vector := to_tsvector('english', COALESCE(NEW.content, ''));
            RETURN NEW;
        END
        $$ LANGUAGE plpgsql;
        
        CREATE TRIGGER update_debate_statement_search_vector
        BEFORE INSERT OR UPDATE ON debate_statements
        FOR EACH ROW EXECUTE FUNCTION update_debate_search_vector();
    """)


def downgrade():
    """Drop debate transcript tables."""
    
    # Drop trigger
    op.execute("DROP TRIGGER IF EXISTS update_debate_statement_search_vector ON debate_statements")
    op.execute("DROP FUNCTION IF EXISTS update_debate_search_vector()")
    
    # Drop tables in reverse order due to foreign key constraints
    op.drop_index('idx_analytics_session', table_name='debate_analytics')
    op.drop_table('debate_analytics')
    
    op.drop_index('idx_topic_category', table_name='debate_topics')
    op.drop_index('idx_topic_slug', table_name='debate_topics')
    op.drop_table('debate_topics')
    
    op.drop_index('idx_search_public', table_name='debate_searches')
    op.drop_index('idx_search_user', table_name='debate_searches')
    op.drop_table('debate_searches')
    
    op.drop_index('idx_annotation_type', table_name='debate_annotations')
    op.drop_index('idx_annotation_statement', table_name='debate_annotations')
    op.drop_table('debate_annotations')
    
    op.drop_table('debate_session_speakers')
    
    op.drop_index('idx_statement_search', table_name='debate_statements')
    op.drop_index('idx_statement_type', table_name='debate_statements')
    op.drop_index('idx_statement_sequence', table_name='debate_statements')
    op.drop_index('idx_statement_speaker', table_name='debate_statements')
    op.drop_index('idx_statement_session', table_name='debate_statements')
    op.drop_table('debate_statements')
    
    op.drop_index('idx_speaker_party', table_name='debate_speakers')
    op.drop_index('idx_speaker_member', table_name='debate_speakers')
    op.drop_index('idx_speaker_name', table_name='debate_speakers')
    op.drop_table('debate_speakers')
    
    op.drop_index('idx_debate_session_search', table_name='debate_sessions')
    op.drop_index('idx_debate_session_number', table_name='debate_sessions')
    op.drop_index('idx_debate_session_parliament', table_name='debate_sessions')
    op.drop_index('idx_debate_session_date', table_name='debate_sessions')
    op.drop_table('debate_sessions')
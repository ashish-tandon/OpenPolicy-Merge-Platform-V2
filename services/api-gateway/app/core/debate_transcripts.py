"""
Core Debate Transcript Service

Business logic for debate transcript functionality.
Implements FEAT-018 Debate Transcripts (P1 priority).
"""

from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, date, time as datetime_time
from uuid import UUID
import re
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, or_, and_, desc, asc, text
from sqlalchemy.dialects.postgresql import TSVECTOR
from fastapi import HTTPException, status
from app.models.debate_transcripts import (
    DebateSession, DebateStatement, DebateSpeaker,
    DebateAnnotation, DebateSearch, DebateTopic,
    DebateAnalytics, debate_session_speakers
)
from app.models.openparliament import Member
from app.models.users import User
from app.schemas.debate_transcripts import (
    SessionCreate, SessionUpdate, StatementCreate, StatementUpdate,
    SpeakerCreate, SpeakerUpdate, AnnotationCreate, AnnotationUpdate,
    SearchCreate, SearchUpdate, TopicCreate, TopicUpdate,
    TranscriptSearchRequest, TranscriptImportRequest
)
import logging
from collections import defaultdict
import json

logger = logging.getLogger(__name__)


class DebateTranscriptService:
    """Service for managing debate transcripts."""
    
    def __init__(self, db: Session):
        self.db = db
    
    # Session CRUD operations
    def create_session(self, session_data: SessionCreate) -> DebateSession:
        """Create new debate session."""
        # Generate document number
        document_number = f"{session_data.parliament_number}-{session_data.session_number}-{session_data.sitting_number}"
        
        # Check for existing session
        existing = self.db.query(DebateSession).filter(
            DebateSession.document_number == document_number
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Session {document_number} already exists"
            )
        
        session = DebateSession(
            **session_data.dict(),
            document_number=document_number
        )
        
        self.db.add(session)
        self.db.commit()
        
        logger.info(f"Created debate session: {document_number}")
        return session
    
    def get_session(self, session_id: UUID) -> DebateSession:
        """Get debate session by ID."""
        session = self.db.query(DebateSession).options(
            joinedload(DebateSession.statements),
            joinedload(DebateSession.speakers)
        ).filter(DebateSession.id == session_id).first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Debate session not found"
            )
        
        return session
    
    def update_session(
        self,
        session_id: UUID,
        session_data: SessionUpdate
    ) -> DebateSession:
        """Update debate session."""
        session = self.get_session(session_id)
        
        for field, value in session_data.dict(exclude_unset=True).items():
            setattr(session, field, value)
        
        self.db.commit()
        return session
    
    def search_sessions(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        parliament_number: Optional[int] = None,
        session_number: Optional[int] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[DebateSession], int]:
        """Search debate sessions."""
        query = self.db.query(DebateSession)
        
        if start_date:
            query = query.filter(DebateSession.sitting_date >= start_date)
        if end_date:
            query = query.filter(DebateSession.sitting_date <= end_date)
        if parliament_number:
            query = query.filter(DebateSession.parliament_number == parliament_number)
        if session_number:
            query = query.filter(DebateSession.session_number == session_number)
        
        total_count = query.count()
        
        # Order by date descending
        query = query.order_by(desc(DebateSession.sitting_date))
        
        # Pagination
        offset = (page - 1) * page_size
        sessions = query.offset(offset).limit(page_size).all()
        
        return sessions, total_count
    
    # Statement CRUD operations
    def create_statement(
        self,
        statement_data: StatementCreate,
        user: Optional[User] = None
    ) -> DebateStatement:
        """Create new debate statement."""
        # Verify session exists
        session = self.get_session(statement_data.session_id)
        
        # Get next sequence number
        max_seq = self.db.query(func.max(DebateStatement.sequence_number)).filter(
            DebateStatement.session_id == statement_data.session_id
        ).scalar() or 0
        
        # Calculate word count
        word_count = len(statement_data.content.split())
        
        statement = DebateStatement(
            **statement_data.dict(exclude={'word_count'}),
            sequence_number=max_seq + 1,
            word_count=word_count
        )
        
        # Update full-text search vector
        statement.search_vector = func.to_tsvector('english', statement.content)
        
        self.db.add(statement)
        
        # Update session statistics
        session.total_statements += 1
        session.total_words += word_count
        
        self.db.commit()
        
        logger.info(f"Created statement {statement.id} in session {session.document_number}")
        return statement
    
    def update_statement(
        self,
        statement_id: UUID,
        statement_data: StatementUpdate,
        user: User
    ) -> DebateStatement:
        """Update debate statement."""
        statement = self.db.query(DebateStatement).filter(
            DebateStatement.id == statement_id
        ).first()
        
        if not statement:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Statement not found"
            )
        
        # Track word count changes
        old_word_count = statement.word_count
        
        for field, value in statement_data.dict(exclude_unset=True).items():
            setattr(statement, field, value)
        
        # Recalculate word count if content changed
        if statement_data.content:
            statement.word_count = len(statement_data.content.split())
            statement.search_vector = func.to_tsvector('english', statement_data.content)
            
            # Update session word count
            session = statement.session
            session.total_words += (statement.word_count - old_word_count)
        
        self.db.commit()
        return statement
    
    def search_statements(
        self,
        search_request: TranscriptSearchRequest
    ) -> Tuple[List[DebateStatement], int, Dict[str, Dict[str, int]]]:
        """Search debate statements with full-text search."""
        query = self.db.query(DebateStatement).join(
            DebateSession
        ).options(
            joinedload(DebateStatement.speaker),
            joinedload(DebateStatement.session)
        )
        
        # Full-text search
        if search_request.query:
            # Use PostgreSQL full-text search
            search_query = func.plainto_tsquery('english', search_request.query)
            query = query.filter(
                DebateStatement.search_vector.match(search_query)
            )
            
            # Add relevance ranking if searching
            if search_request.sort_by == "relevance":
                query = query.add_columns(
                    func.ts_rank(DebateStatement.search_vector, search_query).label('rank')
                )
        
        # Filter by session criteria
        if search_request.parliament_number:
            query = query.filter(DebateSession.parliament_number == search_request.parliament_number)
        if search_request.session_number:
            query = query.filter(DebateSession.session_number == search_request.session_number)
        if search_request.start_date:
            query = query.filter(DebateSession.sitting_date >= search_request.start_date)
        if search_request.end_date:
            query = query.filter(DebateSession.sitting_date <= search_request.end_date)
        
        # Filter by speaker
        if search_request.speaker_ids:
            query = query.filter(DebateStatement.speaker_id.in_(search_request.speaker_ids))
        
        if search_request.speaker_names:
            query = query.join(DebateSpeaker).filter(
                or_(*[DebateSpeaker.normalized_name.ilike(f"%{name}%") for name in search_request.speaker_names])
            )
        
        if search_request.parties:
            query = query.join(DebateSpeaker).filter(DebateSpeaker.party.in_(search_request.parties))
        
        # Filter by statement type
        if search_request.statement_types:
            query = query.filter(DebateStatement.statement_type.in_(search_request.statement_types))
        
        # Filter by topic
        if search_request.topics:
            query = query.filter(
                or_(*[DebateStatement.topic.ilike(f"%{topic}%") for topic in search_request.topics])
            )
        
        # Filter by bill reference
        if search_request.bills:
            query = query.filter(DebateStatement.bill_reference.in_(search_request.bills))
        
        # Get total count
        total_count = query.count()
        
        # Calculate facets
        facets = self._calculate_facets(query)
        
        # Apply sorting
        if search_request.sort_by == "date":
            sort_column = DebateSession.sitting_date
        elif search_request.sort_by == "relevance" and search_request.query:
            sort_column = 'rank'
        else:  # speaker
            sort_column = DebateStatement.speaker_id
        
        if sort_column == 'rank':
            query = query.order_by(desc('rank'))
        elif search_request.sort_order == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))
        
        # Apply pagination
        offset = (search_request.page - 1) * search_request.page_size
        
        if search_request.sort_by == "relevance" and search_request.query:
            # Handle the case with rank column
            results = query.offset(offset).limit(search_request.page_size).all()
            statements = [result[0] if isinstance(result, tuple) else result for result in results]
        else:
            statements = query.offset(offset).limit(search_request.page_size).all()
        
        return statements, total_count, facets
    
    # Speaker management
    def get_or_create_speaker(
        self,
        name: str,
        party: Optional[str] = None,
        riding: Optional[str] = None,
        member_id: Optional[UUID] = None
    ) -> DebateSpeaker:
        """Get existing speaker or create new one."""
        normalized_name = self._normalize_speaker_name(name)
        
        # Try to find existing speaker
        speaker = self.db.query(DebateSpeaker).filter(
            DebateSpeaker.normalized_name == normalized_name
        ).first()
        
        if not speaker:
            # Create new speaker
            speaker = DebateSpeaker(
                name=name,
                normalized_name=normalized_name,
                party=party,
                riding=riding,
                member_id=member_id,
                first_seen=date.today(),
                last_seen=date.today()
            )
            self.db.add(speaker)
            self.db.flush()
            
            logger.info(f"Created new speaker: {name}")
        else:
            # Update speaker info if provided
            if party and not speaker.party:
                speaker.party = party
            if riding and not speaker.riding:
                speaker.riding = riding
            if member_id and not speaker.member_id:
                speaker.member_id = member_id
            speaker.last_seen = date.today()
        
        return speaker
    
    def update_speaker(
        self,
        speaker_id: UUID,
        speaker_data: SpeakerUpdate
    ) -> DebateSpeaker:
        """Update speaker information."""
        speaker = self.db.query(DebateSpeaker).filter(
            DebateSpeaker.id == speaker_id
        ).first()
        
        if not speaker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Speaker not found"
            )
        
        for field, value in speaker_data.dict(exclude_unset=True).items():
            setattr(speaker, field, value)
        
        self.db.commit()
        return speaker
    
    def search_speakers(
        self,
        query: Optional[str] = None,
        party: Optional[str] = None,
        is_active: Optional[bool] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[DebateSpeaker], int]:
        """Search speakers."""
        db_query = self.db.query(DebateSpeaker)
        
        if query:
            search_term = f"%{query}%"
            db_query = db_query.filter(
                or_(
                    DebateSpeaker.name.ilike(search_term),
                    DebateSpeaker.riding.ilike(search_term)
                )
            )
        
        if party:
            db_query = db_query.filter(DebateSpeaker.party == party)
        
        if is_active is not None:
            db_query = db_query.filter(DebateSpeaker.is_active == is_active)
        
        total_count = db_query.count()
        
        # Order by total statements descending
        db_query = db_query.order_by(desc(DebateSpeaker.total_statements))
        
        # Pagination
        offset = (page - 1) * page_size
        speakers = db_query.offset(offset).limit(page_size).all()
        
        return speakers, total_count
    
    # Annotation management
    def add_annotation(
        self,
        annotation_data: AnnotationCreate,
        user: User
    ) -> DebateAnnotation:
        """Add annotation to statement."""
        # Verify statement exists
        statement = self.db.query(DebateStatement).filter(
            DebateStatement.id == annotation_data.statement_id
        ).first()
        
        if not statement:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Statement not found"
            )
        
        annotation = DebateAnnotation(
            **annotation_data.dict(),
            created_by=user.id
        )
        
        self.db.add(annotation)
        self.db.commit()
        
        logger.info(f"Added annotation to statement {statement.id}")
        return annotation
    
    def update_annotation(
        self,
        annotation_id: UUID,
        annotation_data: AnnotationUpdate,
        user: User
    ) -> DebateAnnotation:
        """Update annotation."""
        annotation = self.db.query(DebateAnnotation).filter(
            DebateAnnotation.id == annotation_id
        ).first()
        
        if not annotation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Annotation not found"
            )
        
        # Check permissions
        if annotation.created_by != user.id and not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this annotation"
            )
        
        annotation.content = annotation_data.content
        self.db.commit()
        
        return annotation
    
    # Topic management
    def create_topic(self, topic_data: TopicCreate) -> DebateTopic:
        """Create new topic."""
        # Generate slug
        slug = self._generate_slug(topic_data.name)
        
        # Check for duplicate
        existing = self.db.query(DebateTopic).filter(
            DebateTopic.slug == slug
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Topic with this name already exists"
            )
        
        topic = DebateTopic(
            **topic_data.dict(),
            slug=slug
        )
        
        self.db.add(topic)
        self.db.commit()
        
        return topic
    
    def get_topics(
        self,
        category: Optional[str] = None,
        is_active: bool = True
    ) -> List[DebateTopic]:
        """Get topics."""
        query = self.db.query(DebateTopic)
        
        if category:
            query = query.filter(DebateTopic.category == category)
        
        query = query.filter(DebateTopic.is_active == is_active)
        
        return query.order_by(desc(DebateTopic.mention_count)).all()
    
    # Analytics
    def generate_analytics(self, session_id: UUID) -> DebateAnalytics:
        """Generate analytics for a debate session."""
        session = self.get_session(session_id)
        
        # Check if analytics already exist
        analytics = self.db.query(DebateAnalytics).filter(
            DebateAnalytics.session_id == session_id
        ).first()
        
        if not analytics:
            analytics = DebateAnalytics(session_id=session_id)
            self.db.add(analytics)
        
        start_time = datetime.utcnow()
        
        # Word frequency analysis
        analytics.top_words = self._analyze_word_frequency(session)
        analytics.word_cloud_data = self._generate_word_cloud_data(analytics.top_words)
        
        # Topic distribution
        analytics.topic_distribution = self._analyze_topics(session)
        
        # Sentiment analysis (placeholder - would use NLP library)
        analytics.sentiment_scores = {
            "positive": 0.4,
            "negative": 0.2,
            "neutral": 0.4
        }
        
        # Speaker analysis
        analytics.speaker_time_distribution = self._analyze_speaker_time(session)
        analytics.party_participation = self._analyze_party_participation(session)
        
        # Engagement metrics
        analytics.interruption_count = self._count_interruptions(session)
        analytics.question_count = self._count_questions(session)
        
        # Summary generation (placeholder - would use NLP)
        analytics.auto_summary = self._generate_summary(session)
        analytics.key_points = self._extract_key_points(session)
        
        # Update computation metadata
        analytics.computed_at = datetime.utcnow()
        analytics.computation_time_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
        
        self.db.commit()
        
        logger.info(f"Generated analytics for session {session.document_number}")
        return analytics
    
    # Import functionality
    def import_transcript(
        self,
        import_data: TranscriptImportRequest,
        user: User
    ) -> DebateSession:
        """Import transcript from external source."""
        # Check if session already exists
        document_number = f"{import_data.parliament_number}-{import_data.session_number}-{import_data.sitting_number}"
        existing = self.db.query(DebateSession).filter(
            DebateSession.document_number == document_number
        ).first()
        
        if existing and not import_data.overwrite:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Session {document_number} already exists. Set overwrite=true to replace."
            )
        
        if existing and import_data.overwrite:
            # Delete existing session and all related data
            self.db.delete(existing)
            self.db.flush()
        
        # Create new session
        session_data = SessionCreate(
            parliament_number=import_data.parliament_number,
            session_number=import_data.session_number,
            sitting_number=import_data.sitting_number,
            sitting_date=import_data.sitting_date,
            language=import_data.language,
            source_url=import_data.document_url
        )
        
        session = self.create_session(session_data)
        
        # Parse content based on source type
        if import_data.source == "parlxml":
            statements = self._parse_parlxml(import_data.document_content)
        elif import_data.source == "json":
            statements = self._parse_json(import_data.document_content)
        else:  # legacy
            statements = self._parse_legacy(import_data.document_content)
        
        # Import statements
        for stmt_data in statements:
            # Get or create speaker
            speaker = None
            if stmt_data.get('speaker_name'):
                speaker = self.get_or_create_speaker(
                    name=stmt_data['speaker_name'],
                    party=stmt_data.get('speaker_party'),
                    riding=stmt_data.get('speaker_riding')
                )
            
            # Create statement
            statement = StatementCreate(
                session_id=session.id,
                speaker_id=speaker.id if speaker else None,
                statement_type=stmt_data['type'],
                content=stmt_data['content'],
                timestamp=stmt_data.get('timestamp'),
                topic=stmt_data.get('topic'),
                bill_reference=stmt_data.get('bill_reference')
            )
            
            self.create_statement(statement)
        
        # Update session speaker count
        session.total_speakers = self.db.query(
            func.count(func.distinct(DebateStatement.speaker_id))
        ).filter(
            DebateStatement.session_id == session.id,
            DebateStatement.speaker_id.isnot(None)
        ).scalar()
        
        self.db.commit()
        
        logger.info(f"Imported transcript for session {document_number}")
        return session
    
    # Helper methods
    def _normalize_speaker_name(self, name: str) -> str:
        """Normalize speaker name for matching."""
        # Remove titles
        name = re.sub(r'^(Hon\.|Right Hon\.|Mr\.|Mrs\.|Ms\.|Dr\.)\s+', '', name)
        # Convert to lowercase and remove extra spaces
        return re.sub(r'\s+', ' ', name.lower().strip())
    
    def _generate_slug(self, text: str) -> str:
        """Generate URL-safe slug from text."""
        # Convert to lowercase and replace spaces with hyphens
        slug = text.lower().replace(' ', '-')
        # Remove non-alphanumeric characters
        slug = re.sub(r'[^a-z0-9-]', '', slug)
        # Remove multiple hyphens
        slug = re.sub(r'-+', '-', slug)
        return slug.strip('-')
    
    def _calculate_facets(self, query) -> Dict[str, Dict[str, int]]:
        """Calculate faceted search results."""
        facets = {
            'statement_type': defaultdict(int),
            'party': defaultdict(int),
            'topic': defaultdict(int)
        }
        
        # Get statement type counts
        type_counts = self.db.query(
            DebateStatement.statement_type,
            func.count(DebateStatement.id)
        ).filter(
            DebateStatement.id.in_([s.id for s in query.limit(1000).all()])
        ).group_by(DebateStatement.statement_type).all()
        
        for stmt_type, count in type_counts:
            facets['statement_type'][stmt_type] = count
        
        # More facet calculations would go here...
        
        return facets
    
    def _analyze_word_frequency(self, session: DebateSession) -> List[Dict[str, Any]]:
        """Analyze word frequency in session."""
        # This is a simplified version - in production would use NLTK or spaCy
        word_counts = defaultdict(int)
        
        for statement in session.statements:
            words = statement.content.lower().split()
            for word in words:
                # Skip common words
                if len(word) > 3 and word not in ['that', 'this', 'with', 'from']:
                    word_counts[word] += 1
        
        # Get top 50 words
        top_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:50]
        
        return [
            {"word": word, "count": count, "tfidf_score": count / len(session.statements)}
            for word, count in top_words
        ]
    
    def _generate_word_cloud_data(self, top_words: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate word cloud data from top words."""
        return {
            "words": [
                {"text": w["word"], "value": w["count"]}
                for w in top_words[:30]
            ]
        }
    
    def _analyze_topics(self, session: DebateSession) -> Dict[str, float]:
        """Analyze topic distribution in session."""
        topic_counts = defaultdict(int)
        
        for statement in session.statements:
            if statement.topic:
                topic_counts[statement.topic] += 1
        
        total = sum(topic_counts.values())
        
        return {
            topic: (count / total * 100) if total > 0 else 0
            for topic, count in topic_counts.items()
        }
    
    def _analyze_speaker_time(self, session: DebateSession) -> Dict[str, float]:
        """Analyze speaker time distribution."""
        speaker_words = defaultdict(int)
        
        for statement in session.statements:
            if statement.speaker_id:
                speaker_words[str(statement.speaker_id)] += statement.word_count
        
        # Convert to estimated speaking time (150 words per minute)
        return {
            speaker_id: words / 150
            for speaker_id, words in speaker_words.items()
        }
    
    def _analyze_party_participation(self, session: DebateSession) -> Dict[str, float]:
        """Analyze party participation."""
        party_counts = defaultdict(int)
        
        for statement in session.statements:
            if statement.speaker and statement.speaker.party:
                party_counts[statement.speaker.party] += 1
        
        total = sum(party_counts.values())
        
        return {
            party: (count / total * 100) if total > 0 else 0
            for party, count in party_counts.items()
        }
    
    def _count_interruptions(self, session: DebateSession) -> int:
        """Count interruptions in session."""
        count = 0
        
        for statement in session.statements:
            if statement.interjections:
                count += len(statement.interjections)
        
        return count
    
    def _count_questions(self, session: DebateSession) -> int:
        """Count questions in session."""
        return self.db.query(func.count(DebateStatement.id)).filter(
            DebateStatement.session_id == session.id,
            DebateStatement.statement_type == "question"
        ).scalar()
    
    def _generate_summary(self, session: DebateSession) -> str:
        """Generate automatic summary of session."""
        # Placeholder - would use NLP summarization
        return f"Parliamentary debate on {session.sitting_date} discussing various topics including bills and policy matters."
    
    def _extract_key_points(self, session: DebateSession) -> List[str]:
        """Extract key points from session."""
        # Placeholder - would use NLP key point extraction
        key_points = []
        
        # Get unique topics discussed
        topics = set()
        for statement in session.statements:
            if statement.topic:
                topics.add(statement.topic)
        
        for topic in list(topics)[:5]:
            key_points.append(f"Discussion on {topic}")
        
        return key_points
    
    def _parse_parlxml(self, content: str) -> List[Dict[str, Any]]:
        """Parse Parliament XML format."""
        # Placeholder - would implement actual XML parsing
        return []
    
    def _parse_json(self, content: str) -> List[Dict[str, Any]]:
        """Parse JSON format."""
        try:
            data = json.loads(content)
            return data.get('statements', [])
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid JSON format"
            )
    
    def _parse_legacy(self, content: str) -> List[Dict[str, Any]]:
        """Parse legacy format."""
        # Placeholder - would implement legacy format parsing
        return []


# Dependency injection helper
def get_debate_transcript_service(db: Session) -> DebateTranscriptService:
    """Get debate transcript service instance."""
    return DebateTranscriptService(db)
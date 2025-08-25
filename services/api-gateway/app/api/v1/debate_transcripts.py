"""
Debate Transcript API endpoints.

Implements FEAT-018 Debate Transcripts (P1 priority).
Provides endpoints for parliamentary debate transcripts (Hansard).
"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from datetime import date
import io
import json
from app.database import get_db
from app.core.dependencies import get_current_user_optional, get_current_user, require_permission
from app.core.debate_transcripts import DebateTranscriptService, get_debate_transcript_service
from app.models.users import User
from app.schemas.debate_transcripts import (
    SessionCreate, SessionUpdate, SessionResponse, SessionListResponse,
    StatementCreate, StatementUpdate, StatementResponse, StatementSearchResponse,
    SpeakerCreate, SpeakerUpdate, SpeakerResponse,
    AnnotationCreate, AnnotationUpdate, AnnotationResponse,
    SearchCreate, SearchUpdate, SearchResponse,
    TopicCreate, TopicUpdate, TopicResponse,
    AnalyticsResponse, TranscriptSearchRequest,
    TranscriptImportRequest, TranscriptExportRequest,
    StatementType
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


# Session endpoints
@router.get("/sessions", response_model=SessionListResponse)
async def list_sessions(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    parliament_number: Optional[int] = Query(None, ge=1, le=99),
    session_number: Optional[int] = Query(None, ge=1, le=10),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    List debate sessions with optional filtering.
    
    Provides access to parliamentary debate sessions (Hansard documents).
    """
    service = get_debate_transcript_service(db)
    sessions, total_count = service.search_sessions(
        start_date=start_date,
        end_date=end_date,
        parliament_number=parliament_number,
        session_number=session_number,
        page=page,
        page_size=page_size
    )
    
    return SessionListResponse(
        results=[SessionResponse.from_orm(s) for s in sessions],
        pagination={
            "page": page,
            "page_size": page_size,
            "total": total_count,
            "total_pages": (total_count + page_size - 1) // page_size
        }
    )


@router.get("/sessions/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: UUID,
    db: Session = Depends(get_db)
):
    """Get debate session details."""
    service = get_debate_transcript_service(db)
    session = service.get_session(session_id)
    return SessionResponse.from_orm(session)


@router.post("/sessions", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    session_data: SessionCreate,
    current_user: User = Depends(require_permission("debates", "write")),
    db: Session = Depends(get_db)
):
    """Create new debate session (admin only)."""
    service = get_debate_transcript_service(db)
    session = service.create_session(session_data)
    return SessionResponse.from_orm(session)


@router.put("/sessions/{session_id}", response_model=SessionResponse)
async def update_session(
    session_id: UUID,
    session_data: SessionUpdate,
    current_user: User = Depends(require_permission("debates", "write")),
    db: Session = Depends(get_db)
):
    """Update debate session (admin only)."""
    service = get_debate_transcript_service(db)
    session = service.update_session(session_id, session_data)
    return SessionResponse.from_orm(session)


# Statement endpoints
@router.get("/statements/search", response_model=StatementSearchResponse)
async def search_statements(
    search_request: TranscriptSearchRequest = Depends(),
    db: Session = Depends(get_db)
):
    """
    Search debate statements with full-text search.
    
    Supports searching across all transcripts with various filters.
    """
    service = get_debate_transcript_service(db)
    statements, total_count, facets = service.search_statements(search_request)
    
    # Build response with speaker info
    results = []
    for statement in statements:
        response = StatementResponse.from_orm(statement)
        if statement.speaker:
            response.speaker_name = statement.speaker.name
            response.speaker_party = statement.speaker.party
            response.speaker_riding = statement.speaker.riding
        response.annotation_count = len(statement.annotations)
        results.append(response)
    
    return StatementSearchResponse(
        results=results,
        pagination={
            "page": search_request.page,
            "page_size": search_request.page_size,
            "total": total_count,
            "total_pages": (total_count + search_request.page_size - 1) // search_request.page_size
        },
        facets=facets
    )


@router.get("/sessions/{session_id}/statements", response_model=List[StatementResponse])
async def get_session_statements(
    session_id: UUID,
    statement_type: Optional[StatementType] = Query(None),
    speaker_id: Optional[UUID] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Get statements for a specific session."""
    from app.models.debate_transcripts import DebateStatement
    
    query = db.query(DebateStatement).filter(
        DebateStatement.session_id == session_id
    )
    
    if statement_type:
        query = query.filter(DebateStatement.statement_type == statement_type)
    
    if speaker_id:
        query = query.filter(DebateStatement.speaker_id == speaker_id)
    
    # Order by sequence number
    query = query.order_by(DebateStatement.sequence_number)
    
    statements = query.offset(skip).limit(limit).all()
    
    # Build response with speaker info
    results = []
    for statement in statements:
        response = StatementResponse.from_orm(statement)
        if statement.speaker:
            response.speaker_name = statement.speaker.name
            response.speaker_party = statement.speaker.party
            response.speaker_riding = statement.speaker.riding
        response.annotation_count = len(statement.annotations)
        results.append(response)
    
    return results


@router.post("/statements", response_model=StatementResponse, status_code=status.HTTP_201_CREATED)
async def create_statement(
    statement_data: StatementCreate,
    current_user: User = Depends(require_permission("debates", "write")),
    db: Session = Depends(get_db)
):
    """Create new statement (admin only)."""
    service = get_debate_transcript_service(db)
    statement = service.create_statement(statement_data, current_user)
    
    response = StatementResponse.from_orm(statement)
    if statement.speaker:
        response.speaker_name = statement.speaker.name
        response.speaker_party = statement.speaker.party
        response.speaker_riding = statement.speaker.riding
    
    return response


@router.put("/statements/{statement_id}", response_model=StatementResponse)
async def update_statement(
    statement_id: UUID,
    statement_data: StatementUpdate,
    current_user: User = Depends(require_permission("debates", "write")),
    db: Session = Depends(get_db)
):
    """Update statement (admin only)."""
    service = get_debate_transcript_service(db)
    statement = service.update_statement(statement_id, statement_data, current_user)
    
    response = StatementResponse.from_orm(statement)
    if statement.speaker:
        response.speaker_name = statement.speaker.name
        response.speaker_party = statement.speaker.party
        response.speaker_riding = statement.speaker.riding
    
    return response


# Speaker endpoints
@router.get("/speakers", response_model=List[SpeakerResponse])
async def list_speakers(
    query: Optional[str] = Query(None),
    party: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """List debate speakers."""
    service = get_debate_transcript_service(db)
    speakers, total_count = service.search_speakers(
        query=query,
        party=party,
        is_active=is_active,
        page=page,
        page_size=page_size
    )
    
    return [SpeakerResponse.from_orm(s) for s in speakers]


@router.get("/speakers/{speaker_id}", response_model=SpeakerResponse)
async def get_speaker(
    speaker_id: UUID,
    db: Session = Depends(get_db)
):
    """Get speaker details."""
    from app.models.debate_transcripts import DebateSpeaker
    
    speaker = db.query(DebateSpeaker).filter(
        DebateSpeaker.id == speaker_id
    ).first()
    
    if not speaker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Speaker not found"
        )
    
    return SpeakerResponse.from_orm(speaker)


@router.put("/speakers/{speaker_id}", response_model=SpeakerResponse)
async def update_speaker(
    speaker_id: UUID,
    speaker_data: SpeakerUpdate,
    current_user: User = Depends(require_permission("debates", "write")),
    db: Session = Depends(get_db)
):
    """Update speaker information (admin only)."""
    service = get_debate_transcript_service(db)
    speaker = service.update_speaker(speaker_id, speaker_data)
    return SpeakerResponse.from_orm(speaker)


# Annotation endpoints
@router.get("/statements/{statement_id}/annotations", response_model=List[AnnotationResponse])
async def get_statement_annotations(
    statement_id: UUID,
    db: Session = Depends(get_db)
):
    """Get annotations for a statement."""
    from app.models.debate_transcripts import DebateAnnotation
    
    annotations = db.query(DebateAnnotation).filter(
        DebateAnnotation.statement_id == statement_id
    ).order_by(DebateAnnotation.created_at).all()
    
    # Build response with creator info
    results = []
    for annotation in annotations:
        response = AnnotationResponse.from_orm(annotation)
        response.creator_name = annotation.creator.full_name if annotation.creator else "System"
        results.append(response)
    
    return results


@router.post("/annotations", response_model=AnnotationResponse, status_code=status.HTTP_201_CREATED)
async def create_annotation(
    annotation_data: AnnotationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add annotation to statement."""
    service = get_debate_transcript_service(db)
    annotation = service.add_annotation(annotation_data, current_user)
    
    response = AnnotationResponse.from_orm(annotation)
    response.creator_name = current_user.full_name
    
    return response


@router.put("/annotations/{annotation_id}", response_model=AnnotationResponse)
async def update_annotation(
    annotation_id: UUID,
    annotation_data: AnnotationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update annotation."""
    service = get_debate_transcript_service(db)
    annotation = service.update_annotation(annotation_id, annotation_data, current_user)
    
    response = AnnotationResponse.from_orm(annotation)
    response.creator_name = annotation.creator.full_name if annotation.creator else "System"
    
    return response


# Topic endpoints
@router.get("/topics", response_model=List[TopicResponse])
async def list_topics(
    category: Optional[str] = Query(None),
    is_active: bool = Query(True),
    db: Session = Depends(get_db)
):
    """List debate topics."""
    service = get_debate_transcript_service(db)
    topics = service.get_topics(category=category, is_active=is_active)
    return [TopicResponse.from_orm(t) for t in topics]


@router.post("/topics", response_model=TopicResponse, status_code=status.HTTP_201_CREATED)
async def create_topic(
    topic_data: TopicCreate,
    current_user: User = Depends(require_permission("debates", "write")),
    db: Session = Depends(get_db)
):
    """Create new topic (admin only)."""
    service = get_debate_transcript_service(db)
    topic = service.create_topic(topic_data)
    return TopicResponse.from_orm(topic)


# Analytics endpoints
@router.get("/sessions/{session_id}/analytics", response_model=AnalyticsResponse)
async def get_session_analytics(
    session_id: UUID,
    regenerate: bool = Query(False),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """
    Get analytics for a debate session.
    
    Includes word frequency, topic distribution, speaker analysis, etc.
    """
    from app.models.debate_transcripts import DebateAnalytics
    
    # Check if analytics exist and if regeneration is requested
    if regenerate and current_user and hasattr(current_user, 'is_admin') and current_user.is_admin:
        service = get_debate_transcript_service(db)
        analytics = service.generate_analytics(session_id)
    else:
        analytics = db.query(DebateAnalytics).filter(
            DebateAnalytics.session_id == session_id
        ).first()
        
        if not analytics:
            # Generate on first request
            service = get_debate_transcript_service(db)
            analytics = service.generate_analytics(session_id)
    
    return AnalyticsResponse.from_orm(analytics)


# Saved search endpoints
@router.get("/searches", response_model=List[SearchResponse])
async def list_saved_searches(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List user's saved searches."""
    from app.models.debate_transcripts import DebateSearch
    
    searches = db.query(DebateSearch).filter(
        DebateSearch.user_id == current_user.id
    ).order_by(DebateSearch.created_at.desc()).all()
    
    return [SearchResponse.from_orm(s) for s in searches]


@router.post("/searches", response_model=SearchResponse, status_code=status.HTTP_201_CREATED)
async def save_search(
    search_data: SearchCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Save a search."""
    from app.models.debate_transcripts import DebateSearch
    
    search = DebateSearch(
        **search_data.dict(),
        user_id=current_user.id
    )
    
    db.add(search)
    db.commit()
    
    return SearchResponse.from_orm(search)


@router.put("/searches/{search_id}", response_model=SearchResponse)
async def update_saved_search(
    search_id: UUID,
    search_data: SearchUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update saved search."""
    from app.models.debate_transcripts import DebateSearch
    
    search = db.query(DebateSearch).filter(
        DebateSearch.id == search_id,
        DebateSearch.user_id == current_user.id
    ).first()
    
    if not search:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Search not found"
        )
    
    for field, value in search_data.dict(exclude_unset=True).items():
        setattr(search, field, value)
    
    db.commit()
    
    return SearchResponse.from_orm(search)


# Import/Export endpoints
@router.post("/import", response_model=SessionResponse)
async def import_transcript(
    import_data: TranscriptImportRequest,
    current_user: User = Depends(require_permission("debates", "write")),
    db: Session = Depends(get_db)
):
    """Import transcript from external source (admin only)."""
    service = get_debate_transcript_service(db)
    session = service.import_transcript(import_data, current_user)
    return SessionResponse.from_orm(session)


@router.post("/import/file", response_model=SessionResponse)
async def import_transcript_file(
    file: UploadFile = File(...),
    source: str = Query(..., regex="^(parlxml|json|legacy)$"),
    parliament_number: int = Query(..., ge=1, le=99),
    session_number: int = Query(..., ge=1, le=10),
    sitting_number: int = Query(..., ge=1, le=999),
    sitting_date: date = Query(...),
    language: str = Query("en", regex="^(en|fr)$"),
    overwrite: bool = Query(False),
    current_user: User = Depends(require_permission("debates", "write")),
    db: Session = Depends(get_db)
):
    """Import transcript from uploaded file (admin only)."""
    # Read file content
    content = await file.read()
    document_content = content.decode('utf-8')
    
    import_data = TranscriptImportRequest(
        source=source,
        document_content=document_content,
        parliament_number=parliament_number,
        session_number=session_number,
        sitting_number=sitting_number,
        sitting_date=sitting_date,
        language=language,
        overwrite=overwrite
    )
    
    service = get_debate_transcript_service(db)
    session = service.import_transcript(import_data, current_user)
    return SessionResponse.from_orm(session)


@router.post("/export")
async def export_transcript(
    export_request: TranscriptExportRequest,
    db: Session = Depends(get_db)
):
    """Export transcript in various formats."""
    service = get_debate_transcript_service(db)
    session = service.get_session(export_request.session_id)
    
    if export_request.format == "json":
        # Build JSON export
        data = {
            "session": {
                "id": str(session.id),
                "document_number": session.document_number,
                "parliament_number": session.parliament_number,
                "session_number": session.session_number,
                "sitting_number": session.sitting_number,
                "sitting_date": session.sitting_date.isoformat(),
                "total_statements": session.total_statements,
                "total_words": session.total_words
            },
            "statements": []
        }
        
        for statement in session.statements:
            stmt_data = {
                "sequence_number": statement.sequence_number,
                "type": statement.statement_type,
                "content": statement.content,
                "speaker": {
                    "name": statement.speaker.name if statement.speaker else None,
                    "party": statement.speaker.party if statement.speaker else None,
                    "riding": statement.speaker.riding if statement.speaker else None
                },
                "timestamp": statement.timestamp.isoformat() if statement.timestamp else None,
                "word_count": statement.word_count
            }
            
            if export_request.include_annotations:
                stmt_data["annotations"] = [
                    {
                        "type": ann.annotation_type,
                        "content": ann.content,
                        "is_official": ann.is_official
                    }
                    for ann in statement.annotations
                ]
            
            data["statements"].append(stmt_data)
        
        if export_request.include_analytics and hasattr(session, 'analytics') and session.analytics:
            data["analytics"] = {
                "top_words": session.analytics.top_words,
                "topic_distribution": session.analytics.topic_distribution,
                "sentiment_scores": session.analytics.sentiment_scores,
                "speaker_time_distribution": session.analytics.speaker_time_distribution,
                "party_participation": session.analytics.party_participation
            }
        
        # Return JSON as streaming response
        content = json.dumps(data, indent=2)
        return StreamingResponse(
            io.BytesIO(content.encode('utf-8')),
            media_type="application/json",
            headers={
                "Content-Disposition": f"attachment; filename=hansard_{session.document_number}.json"
            }
        )
    
    elif export_request.format == "txt":
        # Build plain text export
        lines = [
            f"HANSARD - {session.document_number}",
            f"Date: {session.sitting_date}",
            f"Parliament: {session.parliament_number}, Session: {session.session_number}",
            "=" * 80,
            ""
        ]
        
        for statement in session.statements:
            if statement.speaker:
                lines.append(f"{statement.speaker.name} ({statement.speaker.party}):")
            lines.append(statement.content)
            lines.append("")
        
        content = "\n".join(lines)
        return StreamingResponse(
            io.BytesIO(content.encode('utf-8')),
            media_type="text/plain",
            headers={
                "Content-Disposition": f"attachment; filename=hansard_{session.document_number}.txt"
            }
        )
    
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Export format {export_request.format} not yet implemented"
        )
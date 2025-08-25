"""
Core Feedback Service

Business logic for feedback collection functionality.
Implements FEAT-003 Feedback Collection (P1 priority).
"""

from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, or_, and_, desc, asc
from fastapi import HTTPException, status
from app.models.feedback import (
    Feedback, FeedbackAttachment, FeedbackResponse, 
    FeedbackVote, FeedbackTemplate,
    FeedbackType, FeedbackStatus, FeedbackPriority, FeedbackCategory
)
from app.models.users import User
from app.schemas.feedback import (
    FeedbackCreate, FeedbackUpdate, FeedbackAssign,
    FeedbackFilter, AttachmentCreate, ResponseCreate,
    VoteCreate, TemplateCreate, TemplateUpdate,
    FeedbackStats, FeedbackTrends
)
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)


class FeedbackService:
    """Service for managing feedback."""
    
    def __init__(self, db: Session):
        self.db = db
    
    # Feedback CRUD operations
    def create_feedback(
        self, 
        feedback_data: FeedbackCreate,
        user: Optional[User] = None
    ) -> Feedback:
        """Create new feedback."""
        feedback = Feedback(
            **feedback_data.dict(exclude={'user_email', 'user_name'} if user else {}),
            user_id=user.id if user else None,
            user_email=feedback_data.user_email if not user else user.email,
            user_name=feedback_data.user_name if not user else user.full_name
        )
        
        self.db.add(feedback)
        self.db.commit()
        
        logger.info(f"Created feedback: {feedback.id} - {feedback.subject}")
        
        # Send notifications if high priority
        if feedback.type == FeedbackType.BUG_REPORT and feedback.priority == FeedbackPriority.CRITICAL:
            self._notify_admins(feedback)
        
        return feedback
    
    def get_feedback(self, feedback_id: UUID) -> Feedback:
        """Get feedback by ID."""
        feedback = self.db.query(Feedback).options(
            joinedload(Feedback.user),
            joinedload(Feedback.assignee),
            joinedload(Feedback.attachments),
            joinedload(Feedback.responses),
            joinedload(Feedback.votes)
        ).filter(Feedback.id == feedback_id).first()
        
        if not feedback:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Feedback not found"
            )
        
        return feedback
    
    def update_feedback(
        self,
        feedback_id: UUID,
        feedback_data: FeedbackUpdate,
        user: User
    ) -> Feedback:
        """Update feedback."""
        feedback = self.get_feedback(feedback_id)
        
        # Track status changes
        old_status = feedback.status
        
        # Update fields
        for field, value in feedback_data.dict(exclude_unset=True).items():
            setattr(feedback, field, value)
        
        # Handle status transitions
        if old_status != feedback.status:
            if feedback.status == FeedbackStatus.RESOLVED:
                feedback.resolved_at = datetime.utcnow()
            elif feedback.status in [FeedbackStatus.PENDING, FeedbackStatus.IN_REVIEW]:
                feedback.resolved_at = None
        
        self.db.commit()
        logger.info(f"Updated feedback: {feedback.id}")
        
        return feedback
    
    def delete_feedback(self, feedback_id: UUID, user: User) -> None:
        """Delete feedback (soft delete by changing status)."""
        feedback = self.get_feedback(feedback_id)
        
        # Check permissions (only admin or submitter can delete)
        if not (user.is_admin or feedback.user_id == user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this feedback"
            )
        
        feedback.status = FeedbackStatus.CLOSED
        self.db.commit()
        
        logger.info(f"Deleted feedback: {feedback.id}")
    
    # Search and filtering
    def search_feedback(self, filter_params: FeedbackFilter) -> Tuple[List[Feedback], int]:
        """Search feedback with filters."""
        query = self.db.query(Feedback).options(
            joinedload(Feedback.user),
            joinedload(Feedback.assignee)
        )
        
        # Apply filters
        if filter_params.type:
            query = query.filter(Feedback.type == filter_params.type)
        
        if filter_params.category:
            query = query.filter(Feedback.category == filter_params.category)
        
        if filter_params.status:
            query = query.filter(Feedback.status == filter_params.status)
        
        if filter_params.priority:
            query = query.filter(Feedback.priority == filter_params.priority)
        
        if filter_params.user_id:
            query = query.filter(Feedback.user_id == filter_params.user_id)
        
        if filter_params.assigned_to:
            query = query.filter(Feedback.assigned_to == filter_params.assigned_to)
        
        if filter_params.start_date:
            query = query.filter(Feedback.created_at >= filter_params.start_date)
        
        if filter_params.end_date:
            query = query.filter(Feedback.created_at <= filter_params.end_date)
        
        if filter_params.search:
            search_term = f"%{filter_params.search}%"
            query = query.filter(
                or_(
                    Feedback.subject.ilike(search_term),
                    Feedback.description.ilike(search_term)
                )
            )
        
        if filter_params.tags:
            for tag in filter_params.tags:
                query = query.filter(Feedback.tags.contains([tag]))
        
        if filter_params.has_attachments is not None:
            if filter_params.has_attachments:
                query = query.join(FeedbackAttachment).distinct()
            else:
                query = query.outerjoin(FeedbackAttachment).filter(
                    FeedbackAttachment.id.is_(None)
                )
        
        if filter_params.has_responses is not None:
            if filter_params.has_responses:
                query = query.join(FeedbackResponse).distinct()
            else:
                query = query.outerjoin(FeedbackResponse).filter(
                    FeedbackResponse.id.is_(None)
                )
        
        # Get total count
        total_count = query.count()
        
        # Apply sorting
        sort_column = getattr(Feedback, filter_params.sort_by)
        if filter_params.sort_by == "vote_score":
            # Calculate vote score
            vote_subquery = self.db.query(
                FeedbackVote.feedback_id,
                func.sum(FeedbackVote.vote_type).label('vote_score')
            ).group_by(FeedbackVote.feedback_id).subquery()
            
            query = query.outerjoin(
                vote_subquery,
                Feedback.id == vote_subquery.c.feedback_id
            )
            sort_column = vote_subquery.c.vote_score
        
        if filter_params.sort_order == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))
        
        # Apply pagination
        offset = (filter_params.page - 1) * filter_params.page_size
        feedback_items = query.offset(offset).limit(filter_params.page_size).all()
        
        return feedback_items, total_count
    
    # Assignment and workflow
    def assign_feedback(
        self,
        feedback_id: UUID,
        assign_data: FeedbackAssign,
        assigner: User
    ) -> Feedback:
        """Assign feedback to a user."""
        feedback = self.get_feedback(feedback_id)
        
        # Update assignment
        feedback.assigned_to = assign_data.assignee_id
        
        if assign_data.priority:
            feedback.priority = assign_data.priority
        
        # Update status if pending
        if feedback.status == FeedbackStatus.PENDING:
            feedback.status = FeedbackStatus.IN_REVIEW
        
        # Add internal note if provided
        if assign_data.notes:
            response = FeedbackResponse(
                feedback_id=feedback_id,
                user_id=assigner.id,
                message=f"Assigned to user: {assign_data.notes}",
                is_internal=True
            )
            self.db.add(response)
        
        self.db.commit()
        logger.info(f"Assigned feedback {feedback_id} to user {assign_data.assignee_id}")
        
        return feedback
    
    # Responses
    def add_response(
        self,
        feedback_id: UUID,
        response_data: ResponseCreate,
        user: User
    ) -> FeedbackResponse:
        """Add response to feedback."""
        feedback = self.get_feedback(feedback_id)
        
        response = FeedbackResponse(
            feedback_id=feedback_id,
            user_id=user.id,
            **response_data.dict()
        )
        
        self.db.add(response)
        
        # Update feedback status if first public response
        if not response_data.is_internal and feedback.status == FeedbackStatus.PENDING:
            feedback.status = FeedbackStatus.IN_REVIEW
        
        self.db.commit()
        logger.info(f"Added response to feedback {feedback_id}")
        
        return response
    
    def update_response(
        self,
        response_id: UUID,
        message: str,
        user: User
    ) -> FeedbackResponse:
        """Update feedback response."""
        response = self.db.query(FeedbackResponse).filter(
            FeedbackResponse.id == response_id
        ).first()
        
        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Response not found"
            )
        
        # Check permissions
        if response.user_id != user.id and not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this response"
            )
        
        response.message = message
        self.db.commit()
        
        return response
    
    # Voting
    def vote_feedback(
        self,
        feedback_id: UUID,
        vote_data: VoteCreate,
        user: User
    ) -> Dict[str, Any]:
        """Vote on feedback."""
        feedback = self.get_feedback(feedback_id)
        
        # Check for existing vote
        existing_vote = self.db.query(FeedbackVote).filter(
            and_(
                FeedbackVote.feedback_id == feedback_id,
                FeedbackVote.user_id == user.id
            )
        ).first()
        
        if existing_vote:
            if existing_vote.vote_type == vote_data.vote_type:
                # Remove vote if same type (toggle)
                self.db.delete(existing_vote)
            else:
                # Update vote
                existing_vote.vote_type = vote_data.vote_type
        else:
            # Create new vote
            vote = FeedbackVote(
                feedback_id=feedback_id,
                user_id=user.id,
                vote_type=vote_data.vote_type
            )
            self.db.add(vote)
        
        self.db.commit()
        
        # Get updated vote stats
        return self._get_vote_stats(feedback_id, user.id)
    
    # Attachments
    def add_attachment(
        self,
        feedback_id: UUID,
        attachment_data: AttachmentCreate,
        user: User
    ) -> FeedbackAttachment:
        """Add attachment to feedback."""
        feedback = self.get_feedback(feedback_id)
        
        attachment = FeedbackAttachment(
            feedback_id=feedback_id,
            uploaded_by=user.id,
            **attachment_data.dict()
        )
        
        self.db.add(attachment)
        self.db.commit()
        
        logger.info(f"Added attachment to feedback {feedback_id}")
        
        return attachment
    
    def delete_attachment(
        self,
        attachment_id: UUID,
        user: User
    ) -> None:
        """Delete attachment."""
        attachment = self.db.query(FeedbackAttachment).filter(
            FeedbackAttachment.id == attachment_id
        ).first()
        
        if not attachment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Attachment not found"
            )
        
        # Check permissions
        if attachment.uploaded_by != user.id and not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this attachment"
            )
        
        self.db.delete(attachment)
        self.db.commit()
    
    # Templates
    def create_template(
        self,
        template_data: TemplateCreate
    ) -> FeedbackTemplate:
        """Create feedback template."""
        # Check for duplicate name
        existing = self.db.query(FeedbackTemplate).filter(
            FeedbackTemplate.name == template_data.name
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Template with this name already exists"
            )
        
        template = FeedbackTemplate(**template_data.dict())
        self.db.add(template)
        self.db.commit()
        
        return template
    
    def update_template(
        self,
        template_id: UUID,
        template_data: TemplateUpdate
    ) -> FeedbackTemplate:
        """Update feedback template."""
        template = self.db.query(FeedbackTemplate).filter(
            FeedbackTemplate.id == template_id
        ).first()
        
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Template not found"
            )
        
        for field, value in template_data.dict(exclude_unset=True).items():
            setattr(template, field, value)
        
        self.db.commit()
        
        return template
    
    def get_templates(
        self,
        type: Optional[FeedbackType] = None,
        category: Optional[FeedbackCategory] = None,
        active_only: bool = True
    ) -> List[FeedbackTemplate]:
        """Get feedback templates."""
        query = self.db.query(FeedbackTemplate)
        
        if type:
            query = query.filter(FeedbackTemplate.type == type)
        
        if category:
            query = query.filter(FeedbackTemplate.category == category)
        
        if active_only:
            query = query.filter(FeedbackTemplate.is_active == True)
        
        return query.order_by(FeedbackTemplate.name).all()
    
    # Analytics
    def get_feedback_stats(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> FeedbackStats:
        """Get feedback statistics."""
        query = self.db.query(Feedback)
        
        if start_date:
            query = query.filter(Feedback.created_at >= start_date)
        if end_date:
            query = query.filter(Feedback.created_at <= end_date)
        
        feedback_items = query.all()
        
        # Calculate stats
        by_status = defaultdict(int)
        by_type = defaultdict(int)
        by_category = defaultdict(int)
        by_priority = defaultdict(int)
        
        resolution_times = []
        
        for feedback in feedback_items:
            by_status[feedback.status] += 1
            by_type[feedback.type] += 1
            by_category[feedback.category] += 1
            by_priority[feedback.priority] += 1
            
            if feedback.resolved_at and feedback.created_at:
                resolution_time = (feedback.resolved_at - feedback.created_at).total_seconds() / 3600
                resolution_times.append(resolution_time)
        
        # Calculate response rate
        with_responses = self.db.query(Feedback).join(
            FeedbackResponse
        ).filter(
            FeedbackResponse.is_internal == False
        ).distinct().count()
        
        response_rate = (with_responses / len(feedback_items) * 100) if feedback_items else 0
        
        return FeedbackStats(
            total_count=len(feedback_items),
            by_status=dict(by_status),
            by_type=dict(by_type),
            by_category=dict(by_category),
            by_priority=dict(by_priority),
            avg_resolution_time=sum(resolution_times) / len(resolution_times) if resolution_times else None,
            pending_count=by_status[FeedbackStatus.PENDING],
            resolved_count=by_status[FeedbackStatus.RESOLVED],
            response_rate=response_rate
        )
    
    def get_feedback_trends(
        self,
        period: str = "daily",
        days: int = 30
    ) -> FeedbackTrends:
        """Get feedback trends over time."""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Query based on period
        if period == "daily":
            date_trunc = func.date_trunc('day', Feedback.created_at)
        elif period == "weekly":
            date_trunc = func.date_trunc('week', Feedback.created_at)
        else:  # monthly
            date_trunc = func.date_trunc('month', Feedback.created_at)
        
        results = self.db.query(
            date_trunc.label('period'),
            func.count(Feedback.id).label('count'),
            Feedback.type,
            Feedback.status
        ).filter(
            Feedback.created_at >= start_date
        ).group_by(
            date_trunc,
            Feedback.type,
            Feedback.status
        ).all()
        
        # Format results
        trends_data = defaultdict(lambda: {
            'total': 0,
            'by_type': defaultdict(int),
            'by_status': defaultdict(int)
        })
        
        for result in results:
            period_key = result.period.isoformat()
            trends_data[period_key]['total'] += result.count
            trends_data[period_key]['by_type'][result.type] += result.count
            trends_data[period_key]['by_status'][result.status] += result.count
        
        # Convert to list format
        data = [
            {
                'period': period,
                'total': stats['total'],
                'by_type': dict(stats['by_type']),
                'by_status': dict(stats['by_status'])
            }
            for period, stats in sorted(trends_data.items())
        ]
        
        return FeedbackTrends(period=period, data=data)
    
    # Helper methods
    def _get_vote_stats(self, feedback_id: UUID, user_id: UUID) -> Dict[str, Any]:
        """Get vote statistics for feedback."""
        votes = self.db.query(FeedbackVote).filter(
            FeedbackVote.feedback_id == feedback_id
        ).all()
        
        upvotes = sum(1 for v in votes if v.vote_type == 1)
        downvotes = sum(1 for v in votes if v.vote_type == -1)
        user_vote = next((v.vote_type for v in votes if v.user_id == user_id), None)
        
        return {
            'feedback_id': str(feedback_id),
            'user_vote': user_vote,
            'total_score': upvotes - downvotes,
            'upvotes': upvotes,
            'downvotes': downvotes
        }
    
    def _notify_admins(self, feedback: Feedback) -> None:
        """Notify admins of critical feedback."""
        # TODO: Implement notification system
        logger.warning(f"Critical feedback submitted: {feedback.id} - {feedback.subject}")


# Dependency injection helper
def get_feedback_service(db: Session) -> FeedbackService:
    """Get feedback service instance."""
    return FeedbackService(db)
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.database import get_db
from app.models.user_voting import UserVote
from app.schemas.user_voting import UserVoteCreate, UserVoteResponse, UserVoteListResponse, VoteSummaryResponse

router = APIRouter(prefix="/user-voting", tags=["User Voting"])

@router.post("/cast-vote", response_model=UserVoteResponse)
async def cast_bill_vote(
    bill_id: str = Query(..., description="Bill ID to vote on"),
    vote_data: UserVoteCreate = None,
    db: Session = Depends(get_db)
):
    """Cast a user vote on a bill"""
    try:
        # Check if user already voted on this bill
        existing_vote = db.query(UserVote).filter(
            UserVote.user_id == vote_data.user_id,
            UserVote.bill_id == bill_id
        ).first()
        
        if existing_vote:
            # Update existing vote
            existing_vote.vote_choice = vote_data.vote_choice
            existing_vote.reason = vote_data.reason
            existing_vote.confidence_level = vote_data.confidence_level
            existing_vote.constituency = vote_data.constituency
            existing_vote.party_preference = vote_data.party_preference
            existing_vote.influence_factors = vote_data.influence_factors
            existing_vote.related_issues = vote_data.related_issues
            existing_vote.public_visibility = vote_data.public_visibility
            existing_vote.vote_weight = vote_data.vote_weight
            existing_vote.device = vote_data.device
            existing_vote.location = vote_data.location
            existing_vote.session_id = vote_data.session_id
            existing_vote.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(existing_vote)
            
            return UserVoteResponse.from_orm(existing_vote)
        
        # Create new vote
        new_vote = UserVote(
            user_id=vote_data.user_id,
            bill_id=bill_id,
            vote_choice=vote_data.vote_choice,
            reason=vote_data.reason,
            confidence_level=vote_data.confidence_level,
            constituency=vote_data.constituency,
            party_preference=vote_data.party_preference,
            influence_factors=vote_data.influence_factors,
            related_issues=vote_data.related_issues,
            public_visibility=vote_data.public_visibility,
            vote_weight=vote_data.vote_weight,
            device=vote_data.device,
            location=vote_data.location,
            session_id=vote_data.session_id,
            vote_date=datetime.utcnow()
        )
        
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        
        return UserVoteResponse.from_orm(new_vote)
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to cast vote: {str(e)}")

@router.get("/bill/{bill_id}/user-votes", response_model=UserVoteListResponse)
async def get_bill_user_votes(
    bill_id: str,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    public_only: bool = Query(True, description="Show only public votes"),
    db: Session = Depends(get_db)
):
    """Get user votes for a specific bill"""
    try:
        query = db.query(UserVote).filter(UserVote.bill_id == bill_id)
        
        if public_only:
            query = query.filter(UserVote.public_visibility == 'public')
        
        # Get total count
        total_count = query.count()
        
        # Apply pagination
        offset = (page - 1) * page_size
        votes = query.offset(offset).limit(page_size).all()
        
        # Convert to response models
        results = [UserVoteResponse.from_orm(vote) for vote in votes]
        
        return UserVoteListResponse(
            results=results,
            total_count=total_count,
            page=page,
            page_size=page_size,
            total_pages=(total_count + page_size - 1) // page_size
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve user votes: {str(e)}")

@router.get("/user/{user_id}/voting-history", response_model=UserVoteListResponse)
async def get_user_voting_history(
    user_id: str,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Get voting history for a specific user"""
    try:
        query = db.query(UserVote).filter(UserVote.user_id == user_id).order_by(UserVote.vote_date.desc())
        
        # Get total count
        total_count = query.count()
        
        # Apply pagination
        offset = (page - 1) * page_size
        votes = query.offset(offset).limit(page_size).all()
        
        # Convert to response models
        results = [UserVoteResponse.from_orm(vote) for vote in votes]
        
        return UserVoteListResponse(
            results=results,
            total_count=total_count,
            page=page,
            page_size=page_size,
            total_pages=(total_count + page_size - 1) // page_size
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve voting history: {str(e)}")

@router.get("/bill/{bill_id}/voting-summary", response_model=VoteSummaryResponse)
async def get_bill_voting_summary(
    bill_id: str,
    db: Session = Depends(get_db)
):
    """Get comprehensive voting summary for a bill"""
    try:
        # Get all votes for the bill
        all_votes = db.query(UserVote).filter(UserVote.bill_id == bill_id).all()
        
        if not all_votes:
            return VoteSummaryResponse(
                bill_id=bill_id,
                overall_statistics={
                    "total_votes_cast": 0,
                    "yes_votes": 0,
                    "no_votes": 0,
                    "abstentions": 0,
                    "yes_percentage": 0,
                    "no_percentage": 0,
                    "abstain_percentage": 0
                },
                constituency_breakdown={
                    "total_constituencies": 0,
                    "constituencies_with_votes": 0,
                    "constituency_coverage": 0,
                    "top_supporting_constituencies": [],
                    "top_opposing_constituencies": []
                },
                demographic_breakdown={
                    "age_groups": {},
                    "party_preferences": {}
                },
                voting_trends={
                    "peak_voting_time": "Unknown",
                    "voting_momentum": "Unknown",
                    "constituency_spread": "Unknown",
                    "daily_voting": {}
                }
            )
        
        # Calculate overall statistics
        total_votes = len(all_votes)
        yes_votes = len([v for v in all_votes if v.vote_choice == 'yes'])
        no_votes = len([v for v in all_votes if v.vote_choice == 'no'])
        abstentions = len([v for v in all_votes if v.vote_choice == 'abstain'])
        
        overall_stats = {
            "total_votes_cast": total_votes,
            "yes_votes": yes_votes,
            "no_votes": no_votes,
            "abstentions": abstentions,
            "yes_percentage": round((yes_votes / total_votes) * 100, 1) if total_votes > 0 else 0,
            "no_percentage": round((no_votes / total_votes) * 100, 1) if total_votes > 0 else 0,
            "abstain_percentage": round((abstentions / total_votes) * 100, 1) if total_votes > 0 else 0
        }
        
        # Calculate constituency breakdown
        constituencies = {}
        for vote in all_votes:
            if vote.constituency:
                if vote.constituency not in constituencies:
                    constituencies[vote.constituency] = {"yes": 0, "no": 0, "abstain": 0, "total": 0}
                
                constituencies[vote.constituency][vote.vote_choice] += 1
                constituencies[vote.constituency]["total"] += 1
        
        # Calculate constituency statistics
        constituency_stats = []
        for constituency, stats in constituencies.items():
            total = stats["total"]
            yes_pct = round((stats["yes"] / total) * 100, 1) if total > 0 else 0
            no_pct = round((stats["no"] / total) * 100, 1) if total > 0 else 0
            
            constituency_stats.append({
                "name": constituency,
                "total_votes": total,
                "yes_votes": stats["yes"],
                "no_votes": stats["no"],
                "abstentions": stats["abstain"],
                "yes_percentage": yes_pct,
                "no_percentage": no_pct
            })
        
        # Sort constituencies by yes percentage and no percentage
        supporting_constituencies = sorted(constituency_stats, key=lambda x: x["yes_percentage"], reverse=True)[:5]
        opposing_constituencies = sorted(constituency_stats, key=lambda x: x["no_percentage"], reverse=True)[:5]
        
        constituency_breakdown = {
            "total_constituencies": len(constituencies),
            "constituencies_with_votes": len(constituencies),
            "constituency_coverage": round((len(constituencies) / 338) * 100, 1),  # Assuming 338 federal ridings
            "top_supporting_constituencies": supporting_constituencies,
            "top_opposing_constituencies": opposing_constituencies
        }
        
        # Calculate demographic breakdown (simplified)
        party_preferences = {}
        for vote in all_votes:
            if vote.party_preference:
                if vote.party_preference not in party_preferences:
                    party_preferences[vote.party_preference] = {"yes": 0, "no": 0, "abstain": 0, "total": 0}
                
                party_preferences[vote.party_preference][vote.vote_choice] += 1
                party_preferences[vote.party_preference]["total"] += 1
        
        # Calculate party percentages
        for party, stats in party_preferences.items():
            total = stats["total"]
            party_preferences[party] = {
                "yes": round((stats["yes"] / total) * 100, 1) if total > 0 else 0,
                "no": round((stats["no"] / total) * 100, 1) if total > 0 else 0,
                "abstain": round((stats["abstain"] / total) * 100, 1) if total > 0 else 0
            }
        
        demographic_breakdown = {
            "age_groups": {},  # Would need age data from user profiles
            "party_preferences": party_preferences
        }
        
        # Calculate voting trends
        daily_voting = {}
        for vote in all_votes:
            date_str = vote.vote_date.strftime("%Y-%m-%d")
            daily_voting[date_str] = daily_voting.get(date_str, 0) + 1
        
        voting_trends = {
            "peak_voting_time": "Afternoon",  # Simplified
            "voting_momentum": "Steady" if len(daily_voting) > 1 else "Initial",
            "constituency_spread": "Wide" if len(constituencies) > 10 else "Limited",
            "daily_voting": daily_voting
        }
        
        return VoteSummaryResponse(
            bill_id=bill_id,
            overall_statistics=overall_stats,
            constituency_breakdown=constituency_breakdown,
            demographic_breakdown=demographic_breakdown,
            voting_trends=voting_trends
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate voting summary: {str(e)}")

@router.get("/user/{user_id}/voting-recommendations")
async def get_voting_recommendations(
    user_id: str,
    bill_id: Optional[str] = Query(None, description="Specific bill for recommendations"),
    db: Session = Depends(get_db)
):
    """Get personalized voting recommendations for a user"""
    try:
        # Get user's voting history
        user_votes = db.query(UserVote).filter(UserVote.user_id == user_id).all()
        
        if not user_votes:
            return {
                "message": "No voting history available for recommendations",
                "recommendations": []
            }
        
        # Analyze user's voting patterns
        vote_choices = [vote.vote_choice for vote in user_votes]
        yes_count = vote_choices.count('yes')
        no_count = vote_choices.count('no')
        abstain_count = vote_choices.count('abstain')
        
        total_votes = len(vote_choices)
        yes_percentage = (yes_count / total_votes) * 100 if total_votes > 0 else 0
        no_percentage = (no_count / total_votes) * 100 if total_votes > 0 else 0
        
        # Generate recommendations based on patterns
        recommendations = []
        
        if yes_percentage > 60:
            recommendations.append({
                "type": "pattern_analysis",
                "message": "You tend to support bills ({}% yes votes)".format(round(yes_percentage, 1)),
                "confidence": "high"
            })
        elif no_percentage > 60:
            recommendations.append({
                "type": "pattern_analysis",
                "message": "You tend to oppose bills ({}% no votes)".format(round(no_percentage, 1)),
                "confidence": "high"
            })
        
        if abstain_count > 0:
            recommendations.append({
                "type": "engagement_analysis",
                "message": "Consider providing reasons for your votes to improve engagement",
                "confidence": "medium"
            })
        
        # Add general recommendations
        recommendations.extend([
            {
                "type": "best_practice",
                "message": "Review bill details and consider constituent impact before voting",
                "confidence": "high"
            },
            {
                "type": "best_practice",
                "message": "Use tags and notes to organize your voting decisions",
                "confidence": "medium"
            }
        ])
        
        return {
            "user_id": user_id,
            "total_votes": total_votes,
            "voting_pattern": {
                "yes_percentage": round(yes_percentage, 1),
                "no_percentage": round(no_percentage, 1),
                "abstain_percentage": round((abstain_count / total_votes) * 100, 1) if total_votes > 0 else 0
            },
            "recommendations": recommendations
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate recommendations: {str(e)}")

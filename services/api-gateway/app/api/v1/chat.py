"""
Chat API endpoints for OpenPolicy V2.

Provides AI-powered chat functionality for bills and issues.
This is a critical feature that was missing from the current implementation.
"""

from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session as DBSession
from typing import Optional, Dict, Any, List
from datetime import datetime
from app.database import get_db
from app.models.openparliament import Bill, ElectedMember, VoteQuestion, Politician, Party, Riding

router = APIRouter()


@router.get("/get-bill")
async def get_bill_for_chat(
    bill_number: str,
    db: DBSession = Depends(get_db)
):
    """
    Get bill information for AI chat context.
    Provides bill summary and context for chat interactions.
    """
    # Verify bill exists
    bill = db.query(Bill).filter(Bill.number == bill_number).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    # For now, create mock bill data for chat
    # In a full implementation, this would come from the database
    bill_data = {
        "id": str(bill.id),
        "bill_number": bill.number,
        "title": bill.name_en,
        "short_title": bill.short_title_en,
        "summary": f"Bill {bill.number}: {bill.name_en}. This bill addresses {bill.short_title_en} and is currently in {bill.status_code} status.",
        "status": bill.status_code,
        "introduced_date": bill.introduced,
        "is_government_bill": bill.is_government_bill if hasattr(bill, 'is_government_bill') else True,
        "sponsor": {
            "name": "Hon. Member",
            "party": "Government",
            "constituency": "Unknown"
        },
        "key_topics": [
            "policy implementation",
            "regulatory framework",
            "public interest",
            "government oversight"
        ],
        "related_issues": [
            "economic development",
            "social welfare",
            "environmental protection",
            "public safety"
        ],
        "chat_context": {
            "bill_type": "legislation",
            "complexity_level": "moderate",
            "public_interest": "high",
            "controversy_level": "low"
        }
    }
    
    return {
        "success": True,
        "data": bill_data,
        "message": "Bill information retrieved successfully for chat"
    }


@router.get("/get-issue")
async def get_issue_for_chat(
    issue_id: str,
    db: DBSession = Depends(get_db)
):
    """
    Get issue information for AI chat context.
    Provides issue details and context for chat interactions.
    """
    # For now, create mock issue data
    # In a full implementation, this would come from the database
    issue_data = {
        "id": issue_id,
        "name": "Sample Issue",
        "summary": "This is a sample issue for demonstration purposes.",
        "description": "Detailed description of the issue and its implications.",
        "category": "policy",
        "priority": "medium",
        "status": "active",
        "created_date": datetime.utcnow().isoformat(),
        "chat_context": {
            "issue_type": "policy_concern",
            "complexity_level": "moderate",
            "public_interest": "medium",
            "resolution_urgency": "normal"
        }
    }
    
    return {
        "success": True,
        "data": issue_data,
        "message": "Issue information retrieved successfully for chat"
    }


@router.post("/bill-chat")
async def bill_chat(
    chat_data: Dict[str, Any] = Body(..., description="Chat data"),
    db: DBSession = Depends(get_db)
):
    """
    Process AI chat interactions for bills.
    Users can ask questions about bills and get contextual responses.
    """
    # Validate required fields
    required_fields = ["bill_number", "summary", "instruction"]
    for field in required_fields:
        if field not in chat_data:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
    
    bill_number = chat_data["bill_number"]
    summary = chat_data["summary"]
    instruction = chat_data["instruction"]
    
    # Verify bill exists
    bill = db.query(Bill).filter(Bill.number == bill_number).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    # For now, create mock AI responses
    # In a full implementation, this would integrate with an AI service
    ai_response = generate_bill_chat_response(bill_number, summary, instruction)
    
    return {
        "success": True,
        "response": ai_response,
        "bill_info": {
            "number": bill_number,
            "title": bill.name_en,
            "status": bill.status_code
        },
        "chat_metadata": {
            "timestamp": datetime.utcnow().isoformat(),
            "instruction_type": classify_instruction(instruction),
            "response_length": len(ai_response),
            "context_used": ["bill_summary", "bill_status", "user_instruction"]
        }
    }


@router.post("/issue-chat")
async def issue_chat(
    chat_data: Dict[str, Any] = Body(..., description="Chat data"),
    db: DBSession = Depends(get_db)
):
    """
    Process AI chat interactions for issues.
    Users can ask questions about issues and get contextual responses.
    """
    # Validate required fields
    required_fields = ["issue_id", "summary", "instruction"]
    for field in required_fields:
        if field not in chat_data:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
    
    issue_id = chat_data["issue_id"]
    summary = chat_data["summary"]
    instruction = chat_data["instruction"]
    
    # For now, create mock AI responses
    # In a full implementation, this would integrate with an AI service
    ai_response = generate_issue_chat_response(issue_id, summary, instruction)
    
    return {
        "success": True,
        "response": ai_response,
        "issue_info": {
            "id": issue_id,
            "name": "Sample Issue",
            "status": "active"
        },
        "chat_metadata": {
            "timestamp": datetime.utcnow().isoformat(),
            "instruction_type": classify_instruction(instruction),
            "response_length": len(ai_response),
            "context_used": ["issue_summary", "issue_status", "user_instruction"]
        }
    }


@router.get("/chat-suggestions")
async def get_chat_suggestions(
    bill_number: Optional[str] = None,
    issue_id: Optional[str] = None,
    user_role: Optional[str] = None,
    db: DBSession = Depends(get_db)
):
    """
    Get contextual chat suggestions for bills or issues.
    Provides role-based and context-aware suggestions.
    """
    if bill_number:
        # Bill-specific suggestions
        suggestions = generate_bill_chat_suggestions(bill_number, user_role)
        context = "bill"
    elif issue_id:
        # Issue-specific suggestions
        suggestions = generate_issue_chat_suggestions(issue_id, user_role)
        context = "issue"
    else:
        # General suggestions
        suggestions = generate_general_chat_suggestions(user_role)
        context = "general"
    
    return {
        "success": True,
        "suggestions": suggestions,
        "context": context,
        "user_role": user_role,
        "total_suggestions": len(suggestions)
    }


@router.get("/chat-history")
async def get_chat_history(
    user_id: str,
    bill_number: Optional[str] = None,
    issue_id: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    db: DBSession = Depends(get_db)
):
    """
    Get user's chat history for bills or issues.
    Provides paginated chat conversation history.
    """
    # For now, create mock chat history
    # In a full implementation, this would come from the database
    mock_history = generate_mock_chat_history(user_id, bill_number, issue_id, page, page_size)
    
    return {
        "success": True,
        "chat_history": mock_history["conversations"],
        "pagination": mock_history["pagination"],
        "user_id": user_id,
        "context": {
            "bill_number": bill_number,
            "issue_id": issue_id
        }
    }


# Helper functions for generating responses and suggestions

def generate_bill_chat_response(bill_number: str, summary: str, instruction: str) -> str:
    """Generate AI response for bill chat."""
    instruction_lower = instruction.lower()
    
    if "explain" in instruction_lower:
        if "farmer" in instruction_lower:
            return f"Let me explain Bill {bill_number} in farming terms: This bill is like planting a new crop - it's introducing a new policy that will grow over time and affect how things work in your community. Think of it as setting new rules for how the government helps farmers and rural areas."
        elif "5 year old" in instruction_lower or "child" in instruction_lower:
            return f"Bill {bill_number} is like making a new rule in your house! Just like your parents make rules to keep everyone safe and happy, this bill makes rules for the whole country. It's like saying 'everyone should be nice to each other' but for grown-up things."
        else:
            return f"Bill {bill_number} is a piece of proposed legislation that addresses {summary}. It's currently being considered by Parliament and, if passed, would become law affecting various aspects of society and governance."
    
    elif "support" in instruction_lower or "oppose" in instruction_lower:
        return f"Regarding whether to support or oppose Bill {bill_number}: This is a personal decision that depends on how the bill's provisions align with your values and interests. Consider reading the full text, consulting with experts, and understanding both the benefits and potential drawbacks."
    
    elif "impact" in instruction_lower:
        return f"Bill {bill_number} could have several impacts: economic effects on businesses and individuals, social changes in how services are delivered, and potential environmental consequences. The exact impact depends on how the bill is implemented and enforced."
    
    else:
        return f"I understand you're asking about Bill {bill_number}. This bill relates to {summary}. Could you please be more specific about what you'd like to know? I can explain the bill, discuss its potential impacts, or help you understand specific sections."


def generate_issue_chat_response(issue_id: str, summary: str, instruction: str) -> str:
    """Generate AI response for issue chat."""
    instruction_lower = instruction.lower()
    
    if "explain" in instruction_lower:
        return f"Let me explain this issue: {summary}. This is a matter that has been raised by community members and is being considered for potential policy changes or government attention."
    
    elif "resolve" in instruction_lower or "solution" in instruction_lower:
        return f"To resolve this issue, several approaches could be considered: policy changes, community engagement, government intervention, or public awareness campaigns. The best solution depends on the specific circumstances and stakeholder needs."
    
    else:
        return f"I understand you're asking about this issue: {summary}. Could you please be more specific about what you'd like to know? I can explain the issue, discuss potential solutions, or help you understand the current status."


def generate_bill_chat_suggestions(bill_number: str, user_role: Optional[str] = None) -> List[str]:
    """Generate bill-specific chat suggestions."""
    base_suggestions = [
        f"Explain Bill {bill_number} to me",
        f"What are the key points of Bill {bill_number}?",
        f"How will Bill {bill_number} affect me?",
        f"What's the current status of Bill {bill_number}?"
    ]
    
    if user_role == "farmer":
        base_suggestions.extend([
            f"Explain Bill {bill_number} to me as a farmer",
            f"How does Bill {bill_number} affect agriculture?",
            f"What should farmers know about Bill {bill_number}?"
        ])
    elif user_role == "business":
        base_suggestions.extend([
            f"Explain Bill {bill_number} to me as a business owner",
            f"How does Bill {bill_number} affect businesses?",
            f"What are the business implications of Bill {bill_number}?"
        ])
    
    return base_suggestions


def generate_issue_chat_suggestions(issue_id: str, user_role: Optional[str] = None) -> List[str]:
    """Generate issue-specific chat suggestions."""
    return [
        f"Explain this issue to me",
        f"What are the main concerns?",
        f"How can this issue be resolved?",
        f"What's the current status?",
        f"Who is affected by this issue?"
    ]


def generate_general_chat_suggestions(user_role: Optional[str] = None) -> List[str]:
    """Generate general chat suggestions."""
    suggestions = [
        "How can I get involved in politics?",
        "What bills are currently being debated?",
        "How do I contact my representative?",
        "What's the difference between a bill and a law?"
    ]
    
    if user_role == "student":
        suggestions.extend([
            "How can students participate in democracy?",
            "What are youth-focused policies?"
        ])
    elif user_role == "senior":
        suggestions.extend([
            "How do policies affect seniors?",
            "What are senior-specific programs?"
        ])
    
    return suggestions


def classify_instruction(instruction: str) -> str:
    """Classify the type of instruction for analytics."""
    instruction_lower = instruction.lower()
    
    if "explain" in instruction_lower:
        return "explanation_request"
    elif "support" in instruction_lower or "oppose" in instruction_lower:
        return "opinion_request"
    elif "impact" in instruction_lower or "affect" in instruction_lower:
        return "impact_inquiry"
    elif "how" in instruction_lower:
        return "how_to_inquiry"
    elif "what" in instruction_lower:
        return "what_inquiry"
    elif "when" in instruction_lower:
        return "timing_inquiry"
    else:
        return "general_inquiry"


def generate_mock_chat_history(user_id: str, bill_number: Optional[str], issue_id: Optional[str], page: int, page_size: int) -> Dict[str, Any]:
    """Generate mock chat history for demonstration."""
    conversations = []
    
    for i in range(min(page_size, 5)):  # Mock 5 conversations per page
        conversation = {
            "id": f"chat-{page}-{i}",
            "user_id": user_id,
            "context": {
                "bill_number": bill_number,
                "issue_id": issue_id
            },
            "messages": [
                {
                    "id": f"msg-{i}-1",
                    "sender": "user",
                    "text": f"Sample user message {i+1}",
                    "timestamp": datetime.utcnow().isoformat()
                },
                {
                    "id": f"msg-{i}-2",
                    "sender": "ai",
                    "text": f"Sample AI response {i+1}",
                    "timestamp": datetime.utcnow().isoformat()
                }
            ],
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        conversations.append(conversation)
    
    return {
        "conversations": conversations,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": 25,  # Mock total
            "total_pages": 5,
            "has_next": page < 5,
            "has_prev": page > 1
        }
    }

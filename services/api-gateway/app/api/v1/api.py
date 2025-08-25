"""
Main API router for Merge V2 API Gateway
"""

from fastapi import APIRouter

from app.api.v1 import health, entities, users, votes, debates, auth, committees, members, bills, search, websocket, multi_level_government, user_management, email_alerts, house_status, rss_feeds, language_support, data_visualizations, pwa_system, performance_optimization, testing_qa, postal_codes, feature_flags, member_management, feedback, debate_transcripts

api_router = APIRouter()

# Health check endpoints
from app.api.v1 import represent

# Include all endpoint routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(entities.router, prefix="/entities", tags=["entities"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(votes.router, prefix="/votes", tags=["votes"])
api_router.include_router(debates.router, prefix="/debates", tags=["debates"])
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(committees.router, prefix="/committees", tags=["committees"])
api_router.include_router(members.router, prefix="/members", tags=["members"])
api_router.include_router(bills.router, prefix="/bills", tags=["bills"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(postal_codes.router, prefix="/postal-codes", tags=["postal-codes"])
api_router.include_router(websocket.router, prefix="/ws", tags=["websocket"])
api_router.include_router(multi_level_government.router, prefix="/government", tags=["multi-level-government"])
api_router.include_router(user_management.router, prefix="/users", tags=["user-management"])
api_router.include_router(email_alerts.router, prefix="/email", tags=["email-alerts"])
api_router.include_router(house_status.router, prefix="/house", tags=["house-status"])
api_router.include_router(rss_feeds.router, prefix="/rss", tags=["rss-feeds"])
api_router.include_router(language_support.router, prefix="/language", tags=["language-support"])
api_router.include_router(data_visualizations.router, prefix="/visualizations", tags=["data-visualizations"])
api_router.include_router(pwa_system.router, prefix="/pwa", tags=["pwa-system"])
api_router.include_router(performance_optimization.router, prefix="/performance", tags=["performance-optimization"])
api_router.include_router(testing_qa.router, prefix="/qa", tags=["testing-qa"])
api_router.include_router(feature_flags.router, prefix="/feature-flags", tags=["feature-flags"])
api_router.include_router(member_management.router, prefix="/member-management", tags=["member-management"])
api_router.include_router(feedback.router, prefix="/feedback", tags=["feedback"])
api_router.include_router(debate_transcripts.router, prefix="/debate-transcripts", tags=["debate-transcripts"])

api_router.include_router(represent.router, prefix="/represent", tags=["represent"])

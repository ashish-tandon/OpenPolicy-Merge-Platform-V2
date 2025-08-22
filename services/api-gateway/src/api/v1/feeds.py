"""
RSS/Atom feed endpoints
Based on legacy feed implementations from politicians/views.py
"""
from fastapi import APIRouter, Query, Request, Response
from typing import Optional, List
from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom
from sqlalchemy.orm import Session
from fastapi import Depends
from sqlalchemy import desc

from ...database import get_db
from ...models import Bill, Member, Debate, Committee, Vote, Statement

router = APIRouter(prefix="/feeds", tags=["feeds"])

class FeedGenerator:
    """
    RSS feed generator based on legacy feed_wrapper pattern
    """
    def __init__(self, title: str, link: str, description: str):
        self.title = title
        self.link = link
        self.description = description
        self.items = []
    
    def add_item(self, title: str, link: str, description: str, 
                 pubdate: datetime, guid: Optional[str] = None):
        """Add an item to the feed"""
        self.items.append({
            'title': title,
            'link': link,
            'description': description,
            'pubdate': pubdate,
            'guid': guid or link
        })
    
    def generate_rss(self) -> str:
        """Generate RSS 2.0 feed"""
        rss = ET.Element('rss', version='2.0')
        channel = ET.SubElement(rss, 'channel')
        
        # Channel metadata
        ET.SubElement(channel, 'title').text = self.title
        ET.SubElement(channel, 'link').text = self.link
        ET.SubElement(channel, 'description').text = self.description
        ET.SubElement(channel, 'language').text = 'en-ca'
        ET.SubElement(channel, 'lastBuildDate').text = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        
        # Add items
        for item in self.items:
            item_elem = ET.SubElement(channel, 'item')
            ET.SubElement(item_elem, 'title').text = item['title']
            ET.SubElement(item_elem, 'link').text = item['link']
            ET.SubElement(item_elem, 'description').text = item['description']
            ET.SubElement(item_elem, 'pubDate').text = item['pubdate'].strftime('%a, %d %b %Y %H:%M:%S GMT')
            ET.SubElement(item_elem, 'guid').text = item['guid']
        
        # Pretty print
        rough_string = ET.tostring(rss, encoding='str')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

@router.get("/recent-bills")
async def recent_bills_feed(
    request: Request,
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db)
):
    """
    RSS feed for recent bills
    Based on legacy RSS patterns
    """
    # Get recent bills
    bills = db.query(Bill).order_by(desc(Bill.introduced)).limit(limit).all()
    
    # Create feed
    feed = FeedGenerator(
        title="Recent Bills - OpenParliament.ca",
        link=str(request.url_for('recent_bills_feed')),
        description="Recently introduced bills in the Canadian Parliament"
    )
    
    for bill in bills:
        feed.add_item(
            title=f"Bill {bill.number}: {bill.name}",
            link=f"https://openparliament.ca/bills/{bill.session}/{bill.number}/",
            description=f"Introduced on {bill.introduced.strftime('%B %d, %Y') if bill.introduced else 'Unknown'}. "
                       f"Sponsor: {bill.sponsor.name if bill.sponsor else 'Unknown'}",
            pubdate=bill.introduced or datetime.utcnow()
        )
    
    return Response(content=feed.generate_rss(), media_type="application/rss+xml")

@router.get("/recent-debates")
async def recent_debates_feed(
    request: Request,
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db)
):
    """RSS feed for recent debates"""
    debates = db.query(Debate).order_by(desc(Debate.date)).limit(limit).all()
    
    feed = FeedGenerator(
        title="Recent Debates - OpenParliament.ca",
        link=str(request.url_for('recent_debates_feed')),
        description="Recent debates from the House of Commons"
    )
    
    for debate in debates:
        feed.add_item(
            title=debate.h1_en or f"Debate on {debate.date.strftime('%B %d, %Y')}",
            link=f"https://openparliament.ca/debates/{debate.date}/{debate.number}/",
            description=f"Parliament {debate.parliament}, Session {debate.session}. "
                       f"{debate.statement_count} statements.",
            pubdate=datetime.combine(debate.date, datetime.min.time())
        )
    
    return Response(content=feed.generate_rss(), media_type="application/rss+xml")

@router.get("/mp/{mp_slug}/statements")
async def mp_statements_feed(
    request: Request,
    mp_slug: str,
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db)
):
    """
    RSS feed for MP statements
    Direct adaptation of legacy PoliticianStatementFeed
    """
    # Get MP
    mp = db.query(Member).filter(Member.slug == mp_slug).first()
    if not mp:
        return Response(status_code=404)
    
    # Get recent statements
    statements = db.query(Statement).filter(
        Statement.member_id == mp.id
    ).order_by(desc(Statement.time)).limit(limit).all()
    
    feed = FeedGenerator(
        title=f"Statements by {mp.name} - OpenParliament.ca",
        link=f"https://openparliament.ca/politicians/{mp.slug}/",
        description=f"Recent statements in Parliament by {mp.name}"
    )
    
    for statement in statements:
        feed.add_item(
            title=statement.topic or "House statement",
            link=statement.get_absolute_url(),
            description=statement.text_html(),
            pubdate=statement.time
        )
    
    return Response(content=feed.generate_rss(), media_type="application/rss+xml")

@router.get("/mp/{mp_slug}/activity")
async def mp_activity_feed(
    request: Request,
    mp_slug: str,
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db)
):
    """
    RSS feed for MP activity
    Based on legacy PoliticianActivityFeed
    """
    mp = db.query(Member).filter(Member.slug == mp_slug).first()
    if not mp:
        return Response(status_code=404)
    
    feed = FeedGenerator(
        title=f"Activity by {mp.name} - OpenParliament.ca",
        link=f"https://openparliament.ca/politicians/{mp.slug}/",
        description=f"Recent Parliamentary activity by {mp.name}"
    )
    
    # Get recent statements
    statements = db.query(Statement).filter(
        Statement.member_id == mp.id
    ).order_by(desc(Statement.time)).limit(limit).all()
    
    # Get recent votes
    votes = db.query(Vote).filter(
        Vote.member_id == mp.id
    ).order_by(desc(Vote.date)).limit(limit).all()
    
    # Combine and sort by date
    activities = []
    
    for statement in statements:
        activities.append({
            'type': 'statement',
            'title': f"Said: {statement.topic or 'House statement'}",
            'link': statement.get_absolute_url(),
            'description': statement.text_html()[:500] + '...',
            'date': statement.time
        })
    
    for vote in votes:
        activities.append({
            'type': 'vote',
            'title': f"Voted {vote.vote} on {vote.description}",
            'link': f"https://openparliament.ca/votes/{vote.id}/",
            'description': f"Vote #{vote.number}: {vote.description}",
            'date': vote.date
        })
    
    # Sort by date and limit
    activities.sort(key=lambda x: x['date'], reverse=True)
    activities = activities[:limit]
    
    # Add to feed
    for activity in activities:
        feed.add_item(
            title=activity['title'],
            link=activity['link'],
            description=activity['description'],
            pubdate=activity['date']
        )
    
    return Response(content=feed.generate_rss(), media_type="application/rss+xml")

@router.get("/search")
async def search_feed(
    request: Request,
    q: str = Query(..., description="Search query"),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db)
):
    """
    RSS feed for search results
    Based on legacy SearchFeed
    """
    # For now, return a basic search feed
    # In production, this would integrate with the search engine
    
    feed = FeedGenerator(
        title=f"Search results for '{q}' - OpenParliament.ca",
        link=f"https://openparliament.ca/search/?q={q}",
        description=f"Parliamentary search results for '{q}'"
    )
    
    # Add a placeholder item
    feed.add_item(
        title="Search functionality coming soon",
        link="https://openparliament.ca/search/",
        description="Full search integration will be available in the next update",
        pubdate=datetime.utcnow()
    )
    
    return Response(content=feed.generate_rss(), media_type="application/rss+xml")

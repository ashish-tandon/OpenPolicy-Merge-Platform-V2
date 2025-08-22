"""
Data export endpoints with multiple format support
Based on legacy JSON/XML export patterns
"""
from fastapi import APIRouter, Query, HTTPException, Response
from typing import Optional, List, Dict, Any
import csv
import json
import io
from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom
from sqlalchemy.orm import Session
from fastapi import Depends

from ...database import get_db
from ...models import Bill, Member, Debate, Committee, Vote
from .bills import get_bills_list
from .members import get_members_list
from .debates import get_debates_list
from .committees import get_committees_list

router = APIRouter(prefix="/export", tags=["export"])

def serialize_to_csv(data: List[Dict[str, Any]], fields: List[str]) -> str:
    """Convert data to CSV format"""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    
    for item in data:
        # Flatten nested objects
        flat_item = {}
        for field in fields:
            if '.' in field:
                # Handle nested fields like "party.name"
                parts = field.split('.')
                value = item
                for part in parts:
                    value = value.get(part, '') if isinstance(value, dict) else ''
                flat_item[field] = value
            else:
                flat_item[field] = item.get(field, '')
        writer.writerow(flat_item)
    
    return output.getvalue()

def serialize_to_xml(data: List[Dict[str, Any]], root_name: str, item_name: str) -> str:
    """
    Convert data to XML format
    Based on legacy XML export patterns
    """
    root = ET.Element(root_name)
    
    for item in data:
        item_elem = ET.SubElement(root, item_name)
        for key, value in item.items():
            if isinstance(value, dict):
                # Handle nested objects
                nested_elem = ET.SubElement(item_elem, key)
                for nested_key, nested_value in value.items():
                    child_elem = ET.SubElement(nested_elem, nested_key)
                    child_elem.text = str(nested_value) if nested_value is not None else ''
            else:
                elem = ET.SubElement(item_elem, key)
                elem.text = str(value) if value is not None else ''
    
    # Pretty print(X)ML
    rough_string = ET.tostring(root, encoding='str')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

@router.get("/bills")
async def export_bills(
    format: str = Query("json", enum=["json", "csv", "xml"]),
    session: Optional[str] = None,
    status: Optional[str] = None,
    sponsor: Optional[str] = None,
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db)
):
    """
    Export bills data in multiple formats
    Based on legacy JSON export patterns
    """
    # Get bills data
    bills_response = await get_bills_list(
        page=1,
        search=None,
        session=session,
        privatemember=None,
        db=db
    )
    
    bills_data = [
        {
            "id": bill.id,
            "number": bill.number,
            "name": bill.name,
            "session": bill.session,
            "introduced": bill.introduced.isoformat() if bill.introduced else None,
            "sponsor": {
                "id": bill.sponsor_politician_id,
                "name": bill.sponsor.name if bill.sponsor else None
            } if bill.sponsor_politician_id else None,
            "status": bill.status_code,
            "law": bill.law,
            "privatemember": bill.privatemember
        }
        for bill in bills_response["results"][:limit]
    ]
    
    if format == "json":
        return Response(
            content=json.dumps(bills_data, indent=2),
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename=bills_{datetime.now().strftime('%Y%m%d')}.json"}
        )
    elif format == "csv":
        fields = ["id", "number", "name", "session", "introduced", "sponsor.name", "status", "law", "privatemember"]
        csv_content = serialize_to_csv(bills_data, fields)
        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=bills_{datetime.now().strftime('%Y%m%d')}.csv"}
        )
    elif format == "xml":
        xml_content = serialize_to_xml(bills_data, "bills", "bill")
        return Response(
            content=xml_content,
            media_type="application/xml",
            headers={"Content-Disposition": f"attachment; filename=bills_{datetime.now().strftime('%Y%m%d')}.xml"}
        )

@router.get("/members")
async def export_members(
    format: str = Query("json", enum=["json", "csv", "xml"]),
    current: Optional[bool] = None,
    party: Optional[str] = None,
    province: Optional[str] = None,
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db)
):
    """Export members data in multiple formats"""
    members_response = await get_members_list(
        page=1,
        search=None,
        current=current,
        party=party,
        province=province,
        db=db
    )
    
    members_data = [
        {
            "id": member.id,
            "name": member.name,
            "email": member.email,
            "party": {
                "name": member.party.name,
                "short_name": member.party.short_name
            } if member.party else None,
            "riding": {
                "name": member.riding.name,
                "province": member.riding.province
            } if member.riding else None,
            "current": member.current_member
        }
        for member in members_response["results"][:limit]
    ]
    
    if format == "json":
        return Response(
            content=json.dumps(members_data, indent=2),
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename=members_{datetime.now().strftime('%Y%m%d')}.json"}
        )
    elif format == "csv":
        fields = ["id", "name", "email", "party.name", "riding.name", "riding.province", "current"]
        csv_content = serialize_to_csv(members_data, fields)
        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=members_{datetime.now().strftime('%Y%m%d')}.csv"}
        )
    elif format == "xml":
        xml_content = serialize_to_xml(members_data, "members", "member")
        return Response(
            content=xml_content,
            media_type="application/xml",
            headers={"Content-Disposition": f"attachment; filename=members_{datetime.now().strftime('%Y%m%d')}.xml"}
        )

@router.get("/debates")
async def export_debates(
    format: str = Query("json", enum=["json", "csv", "xml"]),
    date_gte: Optional[str] = None,
    date_lte: Optional[str] = None,
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db)
):
    """Export debates data in multiple formats"""
    debates_response = await get_debates_list(
        page=1,
        date_gte=date_gte,
        date_lte=date_lte,
        db=db
    )
    
    debates_data = [
        {
            "id": debate.id,
            "date": debate.date.isoformat(),
            "number": debate.number,
            "parliament": debate.parliament,
            "session": debate.session,
            "title": debate.h1_en or debate.h2_en,
            "statements_count": debate.statement_count
        }
        for debate in debates_response["results"][:limit]
    ]
    
    if format == "json":
        return Response(
            content=json.dumps(debates_data, indent=2),
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename=debates_{datetime.now().strftime('%Y%m%d')}.json"}
        )
    elif format == "csv":
        fields = ["id", "date", "number", "parliament", "session", "title", "statements_count"]
        csv_content = serialize_to_csv(debates_data, fields)
        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=debates_{datetime.now().strftime('%Y%m%d')}.csv"}
        )
    elif format == "xml":
        xml_content = serialize_to_xml(debates_data, "debates", "debate")
        return Response(
            content=xml_content,
            media_type="application/xml",
            headers={"Content-Disposition": f"attachment; filename=debates_{datetime.now().strftime('%Y%m%d')}.xml"}
        )

@router.get("/bulk/{dataset}")
async def bulk_download(
    dataset: str = Query(..., enum=["bills", "members", "debates", "committees", "votes"]),
    format: str = Query("json", enum=["json", "csv", "xml"]),
    db: Session = Depends(get_db)
):
    """
    Bulk download endpoint for large datasets
    Based on legacy bulk export patterns
    """
    # For bulk downloads, we bypass pagination
    if dataset == "bills":
        return await export_bills(format=format, limit=10000, db=db)
    elif dataset == "members":
        return await export_members(format=format, limit=5000, db=db)
    elif dataset == "debates":
        return await export_debates(format=format, limit=1000, db=db)
    else:
        raise HTTPException(status_code=400, detail=f"Bulk download not available for {dataset}")

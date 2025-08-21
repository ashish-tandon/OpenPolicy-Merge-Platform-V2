"""
Pupa Compatibility Layer for OpenParliament.ca V2
Following FUNDAMENTAL RULE: Fixing legacy scraper compatibility issues
"""
import datetime
from typing import Any, Optional, Union
from dateutil import parser as date_parser

# Mock DatetimeValidator class that legacy scrapers expect
class DatetimeValidator:
    """Compatibility class for legacy scrapers that expect DatetimeValidator"""
    
    def __init__(self, *args, **kwargs):
        pass
    
    def clean(self, value: Any) -> Optional[datetime.datetime]:
        """Clean and validate datetime values"""
        if not value:
            return None
        
        if isinstance(value, datetime.datetime):
            return value
        
        if isinstance(value, str):
            try:
                return date_parser.parse(value)
            except (ValueError, TypeError):
                return None
        
        return None

# Mock other missing utilities
class JurisdictionValidator:
    """Compatibility class for jurisdiction validation"""
    
    def __init__(self, *args, **kwargs):
        pass
    
    def clean(self, value: Any) -> Any:
        """Clean jurisdiction values"""
        return value

class PersonValidator:
    """Compatibility class for person validation"""
    
    def __init__(self, *args, **kwargs):
        pass
    
    def clean(self, value: Any) -> Any:
        """Clean person values"""
        return value

class OrganizationValidator:
    """Compatibility class for organization validation"""
    
    def __init__(self, *args, **kwargs):
        pass
    
    def clean(self, value: Any) -> Any:
        """Clean organization values"""
        return value

class BillValidator:
    """Compatibility class for bill validation"""
    
    def __init__(self, *args, **kwargs):
        pass
    
    def clean(self, value: Any) -> Any:
        """Clean bill values"""
        return value

class VoteValidator:
    """Compatibility class for vote validation"""
    
    def __init__(self, *args, **kwargs):
        pass
    
    def clean(self, value: Any) -> Any:
        """Clean vote values"""
        return value

class VoteEventValidator:
    """Compatibility class for vote event validation"""
    
    def __init__(self, *args, **kwargs):
        pass
    
    def clean(self, value: Any) -> Any:
        """Clean vote event values"""
        return value

class EventValidator:
    """Compatibility class for event validation"""
    
    def __init__(self, *args, **kwargs):
        pass
    
    def clean(self, value: Any) -> Any:
        """Clean event values"""
        return value

class MembershipValidator:
    """Compatibility class for membership validation"""
    
    def __init__(self, *args, **kwargs):
        pass
    
    def clean(self, value: Any) -> Any:
        """Clean membership values"""
        return value

class PostValidator:
    """Compatibility class for post validation"""
    
    def __init__(self, *args, **kwargs):
        pass
    
    def clean(self, value: Any) -> Any:
        """Clean post values"""
        return value

class ContactDetailValidator:
    """Compatibility class for contact detail validation"""
    
    def __init__(self, *args, **kwargs):
        pass
    
    def clean(self, value: Any) -> Any:
        """Clean contact detail values"""
        return value

class IdentifierValidator:
    """Compatibility class for identifier validation"""
    
    def __init__(self, *args, **kwargs):
        pass
    
    def clean(self, value: Any) -> Any:
        """Clean identifier values"""
        return value

class LinkValidator:
    """Compatibility class for link validation"""
    
    def __init__(self, *args, **kwargs):
        pass
    
    def clean(self, value: Any) -> Any:
        """Clean link values"""
        return value

class SourceValidator:
    """Compatibility class for source validation"""
    
    def __init__(self, *args, **kwargs):
        pass
    
    def clean(self, value: Any) -> Any:
        """Clean source values"""
        return value

# Add these to pupa.utils module to fix import errors
def patch_pupa_utils():
    """Patch pupa.utils with missing compatibility classes"""
    import pupa.utils
    
    # Add missing validator classes
    pupa.utils.DatetimeValidator = DatetimeValidator
    pupa.utils.JurisdictionValidator = JurisdictionValidator
    pupa.utils.PersonValidator = PersonValidator
    pupa.utils.OrganizationValidator = OrganizationValidator
    pupa.utils.BillValidator = BillValidator
    pupa.utils.VoteValidator = VoteValidator
    pupa.utils.VoteEventValidator = VoteEventValidator
    pupa.utils.EventValidator = EventValidator
    pupa.utils.MembershipValidator = MembershipValidator
    pupa.utils.PostValidator = PostValidator
    pupa.utils.ContactDetailValidator = ContactDetailValidator
    pupa.utils.IdentifierValidator = IdentifierValidator
    pupa.utils.LinkValidator = LinkValidator
    pupa.utils.SourceValidator = SourceValidator
    
    return pupa.utils

# Auto-patch when module is imported
patch_pupa_utils()

"""
API versioning support
Based on legacy URL patterns and best practices
"""
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, List, Optional
import re

class APIVersion:
    """Represents an API version with its routes"""
    def __init__(self, version: str, router: APIRouter, deprecated: bool = False):
        self.version = version
        self.router = router
        self.deprecated = deprecated
        self.deprecation_date = None
        self.sunset_date = None
    
    def set_deprecation(self, deprecation_date: str, sunset_date: str):
        """Mark version as deprecated with dates"""
        self.deprecated = True
        self.deprecation_date = deprecation_date
        self.sunset_date = sunset_date

class APIVersionManager:
    """
    Manages multiple API versions
    Based on legacy URL versioning patterns
    """
    def __init__(self):
        self.versions: Dict[str, APIVersion] = {}
        self.default_version = None
        self.latest_version = None
    
    def register_version(self, version: str, router: APIRouter, 
                        is_default: bool = False, deprecated: bool = False) -> APIVersion:
        """Register a new API version"""
        api_version = APIVersion(version, router, deprecated)
        self.versions[version] = api_version
        
        if is_default:
            self.default_version = version
        
        # Update latest version (assuming semantic versioning)
        if not self.latest_version or self._compare_versions(version, self.latest_version) > 0:
            self.latest_version = version
        
        return api_version
    
    def _compare_versions(self, v1: str, v2: str) -> int:
        """Compare semantic versions"""
        v1_parts = [int(x) for x in v1.lstrip('v').split('.')]
        v2_parts = [int(x) for x in v2.lstrip('v').split('.')]
        
        for i in range(max(len(v1_parts), len(v2_parts))):
            v1_part = v1_parts[i] if i < len(v1_parts) else 0
            v2_part = v2_parts[i] if i < len(v2_parts) else 0
            
            if v1_part > v2_part:
                return 1
            elif v1_part < v2_part:
                return -1
        
        return 0
    
    def get_version_router(self, version: str) -> Optional[APIRouter]:
        """Get router for a specific version"""
        if version in self.versions:
            return self.versions[version].router
        return None
    
    def get_deprecation_headers(self, version: str) -> Dict[str, str]:
        """Get deprecation headers for a version"""
        headers = {}
        
        if version in self.versions and self.versions[version].deprecated:
            api_version = self.versions[version]
            headers['Deprecation'] = 'true'
            headers['Link'] = f'</api/{self.latest_version}>; rel="successor-version"'
            
            if api_version.sunset_date:
                headers['Sunset'] = api_version.sunset_date
        
        return headers

# Global version manager
version_manager = APIVersionManager()

async def version_middleware(request: Request, call_next):
    """
    Middleware to handle API versioning
    Adds version headers and handles deprecated versions
    """
    # Extract version from path
    path_match = re.match(r'/api/(v\d+(?:\.\d+)?)', request.url.path)
    
    if path_match:
        version = path_match.group(1)
        
        # Check if version exists
        if version not in version_manager.versions:
            return JSONResponse(
                status_code=404,
                content={
                    "error": f"API version {version} not found",
                    "available_versions": list(version_manager.versions.keys()),
                    "latest_version": version_manager.latest_version
                }
            )
        
        # Add version info to request state
        request.state.api_version = version
        
        # Process request
        response = await call_next(request)
        
        # Add version headers
        response.headers['X-API-Version'] = version
        
        # Add deprecation headers if applicable
        deprecation_headers = version_manager.get_deprecation_headers(version)
        for header, value in deprecation_headers.items():
            response.headers[header] = value
        
        return response
    
    # No version specified, use default
    response = await call_next(request)
    response.headers['X-API-Version'] = version_manager.default_version or 'v1'
    
    return response

def create_versioned_app(app):
    """
    Set up API versioning for the FastAPI app
    Based on legacy URL patterns
    """
    # Import v1 routes
    from ..api import v1
    
    # Register v1
    v1_router = APIRouter()
    v1_router.include_router(v1.bills.router)
    v1_router.include_router(v1.members.router)
    v1_router.include_router(v1.debates.router)
    v1_router.include_router(v1.committees.router)
    v1_router.include_router(v1.votes.router)
    v1_router.include_router(v1.export.router)
    v1_router.include_router(v1.feeds.router)
    
    version_manager.register_version('v1', v1_router, is_default=True)
    
    # Mount versioned routes
    for version, api_version in version_manager.versions.items():
        app.include_router(
            api_version.router,
            prefix=f"/api/{version}",
            tags=[f"API {version}"]
        )
    
    # Add version discovery endpoint
    @app.get("/api/versions")
    async def get_api_versions():
        """List available API versions"""
        return {
            "versions": [
                {
                    "version": version,
                    "deprecated": api_version.deprecated,
                    "deprecation_date": api_version.deprecation_date,
                    "sunset_date": api_version.sunset_date,
                    "links": {
                        "self": f"/api/{version}",
                        "docs": f"/api/{version}/docs"
                    }
                }
                for version, api_version in version_manager.versions.items()
            ],
            "default": version_manager.default_version,
            "latest": version_manager.latest_version
        }

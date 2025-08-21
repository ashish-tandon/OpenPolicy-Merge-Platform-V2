"""
ETL Service Main Application

Provides FastAPI endpoints for data extraction, transformation, and loading operations.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="ETL Service",
    description="Data extraction, transformation, and loading service for OpenPolicy Platform",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "ETL Service",
        "version": "0.1.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "etl-service",
        "version": "0.1.0"
    }

@app.get("/status")
async def get_status():
    """Get ETL service status"""
    return {
        "status": "operational",
        "active_tasks": 0,
        "queued_tasks": 0,
        "completed_tasks": 0,
        "failed_tasks": 0
    }

@app.post("/ingest/municipal")
async def ingest_municipal_data():
    """Ingest municipal data"""
    try:
        # Placeholder for municipal data ingestion
        logger.info("Municipal data ingestion requested")
        return {
            "status": "success",
            "message": "Municipal data ingestion started",
            "task_id": "municipal_001"
        }
    except Exception as e:
        logger.error(f"Error in municipal data ingestion: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest/legacy")
async def ingest_legacy_data():
    """Ingest legacy data"""
    try:
        # Placeholder for legacy data ingestion
        logger.info("Legacy data ingestion requested")
        return {
            "status": "success",
            "message": "Legacy data ingestion started",
            "task_id": "legacy_001"
        }
    except Exception as e:
        logger.error(f"Error in legacy data ingestion: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8083)

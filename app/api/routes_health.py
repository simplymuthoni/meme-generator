from fastapi import APIRouter
from app.config.settings import settings
from app.utils.ai_client import ai_client

router = APIRouter()


@router.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "endpoints": {
            "health": "/health",
            "meme_generation": "/api/meme/generate",
            "available_templates": "/api/meme/templates",
            "docs": "/docs"
        }
    }


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "ai_configured": ai_client.is_configured(),
        "app_name": settings.app_name,
        "version": settings.app_version
    }

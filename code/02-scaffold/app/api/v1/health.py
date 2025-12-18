"""
Health Check Endpoint
Lab 2 Complete: Basic health check for the service.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint for load balancers and monitoring."""
    return {
        "status": "healthy",
        "service": "order-service",
        "version": "1.0.0"
    }

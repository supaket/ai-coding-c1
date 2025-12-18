"""
Order Service - FastAPI Application
Lab 2 Complete: Project scaffolding with models and schemas.

Run: uvicorn app.main:app --reload
Docs: http://localhost:8000/docs
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.database import engine, Base
from app.api.v1 import health


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown."""
    # Startup: Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: cleanup if needed
    await engine.dispose()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Order Service",
        description="Microservice for order management - migrated from ShopFast monolith",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan
    )
    
    # Include routers
    app.include_router(health.router, prefix="/api/v1", tags=["Health"])
    
    # TODO Lab 3: Add orders router
    # from app.api.v1 import orders
    # app.include_router(orders.router, prefix="/api/v1", tags=["Orders"])
    
    @app.get("/", tags=["Root"])
    async def root():
        return {
            "message": "Order Service API",
            "docs": "/docs",
            "health": "/api/v1/health"
        }
    
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

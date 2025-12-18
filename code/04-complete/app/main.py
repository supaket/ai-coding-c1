"""ShopFast API - FastAPI Application.

Full microservice with Users, Products, Orders, Inventory, and Notifications.

Run: uvicorn app.main:app --reload
Docs: http://localhost:8000/docs
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import engine, Base
from app.api.v1 import health, orders, users, products, inventory, notifications


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
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
        title="ShopFast API",
        description="E-commerce microservice with full API endpoints",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # Include routers
    app.include_router(health.router, prefix="/api/v1", tags=["Health"])
    app.include_router(users.router, prefix="/api/v1", tags=["Users"])
    app.include_router(products.router, prefix="/api/v1", tags=["Products"])
    app.include_router(orders.router, prefix="/api/v1", tags=["Orders"])
    app.include_router(inventory.router, prefix="/api/v1", tags=["Inventory"])
    app.include_router(notifications.router, prefix="/api/v1", tags=["Notifications"])

    @app.get("/", tags=["Root"])
    async def root() -> dict[str, str]:
        return {
            "message": "ShopFast API",
            "docs": "/docs",
            "health": "/api/v1/health",
        }

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

"""
Products API Endpoints
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.exceptions import ProductNotFoundError
from app.repositories.product_repository import ProductRepository
from app.services.product_service import ProductService
from app.schemas import (
    ProductCreate,
    ProductResponse,
    ErrorResponse,
)

router = APIRouter()


def get_product_service(session: AsyncSession = Depends(get_async_session)) -> ProductService:
    """Dependency to get ProductService instance."""
    repository = ProductRepository(session)
    return ProductService(repository)


@router.get(
    "/products",
    response_model=list[ProductResponse]
)
async def list_products(
    category: Optional[str] = Query(None, description="Filter by category"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    service: ProductService = Depends(get_product_service)
):
    """List all products with optional filtering."""
    products, _ = await service.list_products(
        category=category,
        page=page,
        page_size=page_size
    )
    return products


@router.get(
    "/products/{product_id}",
    response_model=ProductResponse,
    responses={404: {"model": ErrorResponse}}
)
async def get_product(
    product_id: int,
    service: ProductService = Depends(get_product_service)
):
    """Get product details by ID."""
    try:
        product = await service.get_product(product_id)
        return product
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post(
    "/products",
    response_model=ProductResponse,
    status_code=201
)
async def create_product(
    data: ProductCreate,
    service: ProductService = Depends(get_product_service)
):
    """Create a new product."""
    product = await service.create_product(data)
    return product

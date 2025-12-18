"""
Inventory API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.exceptions import ProductNotFoundError
from app.repositories.product_repository import ProductRepository
from app.services.product_service import ProductService
from app.schemas import (
    ProductResponse,
    ProductStockUpdate,
    LowStockItem,
    BulkRestockRequest,
    BulkRestockResponse,
    ErrorResponse,
)

router = APIRouter()


def get_product_service(session: AsyncSession = Depends(get_async_session)) -> ProductService:
    """Dependency to get ProductService instance."""
    repository = ProductRepository(session)
    return ProductService(repository)


@router.get(
    "/inventory/low-stock",
    response_model=list[LowStockItem]
)
async def get_low_stock_items(
    threshold: int = Query(10, ge=1, description="Stock threshold"),
    service: ProductService = Depends(get_product_service)
):
    """Get products with low stock (below threshold)."""
    products = await service.get_low_stock_items(threshold)
    return products


@router.put(
    "/inventory/{product_id}",
    response_model=ProductResponse,
    responses={404: {"model": ErrorResponse}}
)
async def update_stock(
    product_id: int,
    data: ProductStockUpdate,
    service: ProductService = Depends(get_product_service)
):
    """Update product stock level."""
    try:
        product = await service.update_stock(product_id, data.stock)
        return product
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post(
    "/inventory/restock",
    response_model=BulkRestockResponse,
    responses={404: {"model": ErrorResponse}}
)
async def bulk_restock(
    data: BulkRestockRequest,
    service: ProductService = Depends(get_product_service)
):
    """Bulk restock multiple products."""
    try:
        products = await service.bulk_restock(data)
        return BulkRestockResponse(
            updated_count=len(products),
            items=products
        )
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

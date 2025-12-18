"""
Orders API Endpoints
Lab 3 Complete: FastAPI router with full CRUD operations.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.exceptions import (
    OrderNotFoundError,
    InvalidStatusTransitionError,
    OrderCancellationError
)
from app.repositories.order_repository import OrderRepository
from app.services.order_service import OrderService
from app.schemas import (
    OrderCreate,
    OrderUpdate,
    OrderResponse,
    OrderSummary,
    PaginatedOrders,
    ErrorResponse
)

router = APIRouter()


def get_order_service(session: AsyncSession = Depends(get_async_session)) -> OrderService:
    """Dependency to get OrderService instance."""
    repository = OrderRepository(session)
    return OrderService(repository)


@router.post(
    "/orders",
    response_model=OrderResponse,
    status_code=201,
    responses={400: {"model": ErrorResponse}}
)
async def create_order(
    data: OrderCreate,
    service: OrderService = Depends(get_order_service)
):
    """Create a new order with items."""
    order = await service.create_order(data)
    return order


@router.get(
    "/orders",
    response_model=PaginatedOrders
)
async def list_orders(
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    service: OrderService = Depends(get_order_service)
):
    """List orders with optional filtering and pagination."""
    orders, total = await service.list_orders(
        user_id=user_id,
        status=status,
        page=page,
        page_size=page_size
    )
    return PaginatedOrders(
        items=[OrderSummary.model_validate(o) for o in orders],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get(
    "/orders/{order_id}",
    response_model=OrderResponse,
    responses={404: {"model": ErrorResponse}}
)
async def get_order(
    order_id: int,
    service: OrderService = Depends(get_order_service)
):
    """Get order details by ID."""
    try:
        order = await service.get_order(order_id)
        return order
    except OrderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch(
    "/orders/{order_id}",
    response_model=OrderResponse,
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse}
    }
)
async def update_order(
    order_id: int,
    data: OrderUpdate,
    service: OrderService = Depends(get_order_service)
):
    """Update order status or details."""
    try:
        order = await service.update_order(order_id, data)
        return order
    except OrderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidStatusTransitionError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/orders/{order_id}/cancel",
    response_model=OrderResponse,
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse}
    }
)
async def cancel_order(
    order_id: int,
    service: OrderService = Depends(get_order_service)
):
    """Cancel an order."""
    try:
        order = await service.cancel_order(order_id)
        return order
    except OrderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except OrderCancellationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/users/{user_id}/orders",
    response_model=list[OrderResponse]
)
async def get_user_orders(
    user_id: int,
    service: OrderService = Depends(get_order_service)
):
    """Get all orders for a specific user."""
    orders = await service.get_user_orders(user_id)
    return orders

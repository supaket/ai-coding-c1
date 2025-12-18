"""
Unit Tests for Order Service
Lab 4 Complete: Testing business logic layer.
"""

import pytest
from decimal import Decimal

from app.models import Order, OrderStatus
from app.schemas import OrderCreate, OrderUpdate, OrderItemCreate
from app.repositories.order_repository import OrderRepository
from app.services.order_service import OrderService
from app.core.exceptions import (
    OrderNotFoundError,
    InvalidStatusTransitionError,
    OrderCancellationError
)


class TestCreateOrder:
    """Tests for order creation."""
    
    @pytest.mark.asyncio
    async def test_create_order_calculates_total(self, test_session):
        """Order total should be sum of item prices × quantities."""
        repository = OrderRepository(test_session)
        service = OrderService(repository)
        
        data = OrderCreate(
            user_id=1,
            shipping_address="123 Test St",
            items=[
                OrderItemCreate(product_id=1, quantity=1),  # $1299.99
                OrderItemCreate(product_id=2, quantity=2),  # $49.99 × 2
            ]
        )
        
        order = await service.create_order(data)
        
        assert order.total == Decimal("1399.97")
        assert len(order.items) == 2
    
    @pytest.mark.asyncio
    async def test_create_order_sets_pending_status(self, test_session):
        """New orders should have pending status."""
        repository = OrderRepository(test_session)
        service = OrderService(repository)
        
        data = OrderCreate(
            user_id=1,
            items=[OrderItemCreate(product_id=1, quantity=1)]
        )
        
        order = await service.create_order(data)
        
        assert order.status == OrderStatus.PENDING.value


class TestGetOrder:
    """Tests for getting orders."""
    
    @pytest.mark.asyncio
    async def test_get_existing_order(self, test_session, sample_order):
        """Should return order when it exists."""
        repository = OrderRepository(test_session)
        service = OrderService(repository)
        
        order = await service.get_order(sample_order.id)
        
        assert order.id == sample_order.id
        assert order.user_id == sample_order.user_id
    
    @pytest.mark.asyncio
    async def test_get_nonexistent_order_raises_error(self, test_session):
        """Should raise OrderNotFoundError for invalid ID."""
        repository = OrderRepository(test_session)
        service = OrderService(repository)
        
        with pytest.raises(OrderNotFoundError) as exc:
            await service.get_order(99999)
        
        assert exc.value.order_id == 99999


class TestUpdateOrder:
    """Tests for order updates."""
    
    @pytest.mark.asyncio
    async def test_valid_status_transition(self, test_session, sample_order):
        """Should allow valid status transitions."""
        repository = OrderRepository(test_session)
        service = OrderService(repository)
        
        data = OrderUpdate(status=OrderStatus.CONFIRMED)
        order = await service.update_order(sample_order.id, data)
        
        assert order.status == OrderStatus.CONFIRMED.value
    
    @pytest.mark.asyncio
    async def test_invalid_status_transition_raises_error(self, test_session, sample_order):
        """Should reject invalid status transitions."""
        repository = OrderRepository(test_session)
        service = OrderService(repository)
        
        # Can't go from pending directly to delivered
        data = OrderUpdate(status=OrderStatus.DELIVERED)
        
        with pytest.raises(InvalidStatusTransitionError):
            await service.update_order(sample_order.id, data)
    
    @pytest.mark.asyncio
    async def test_update_shipping_address(self, test_session, sample_order):
        """Should update shipping address."""
        repository = OrderRepository(test_session)
        service = OrderService(repository)
        
        data = OrderUpdate(shipping_address="456 New Address")
        order = await service.update_order(sample_order.id, data)
        
        assert order.shipping_address == "456 New Address"


class TestCancelOrder:
    """Tests for order cancellation."""
    
    @pytest.mark.asyncio
    async def test_cancel_pending_order(self, test_session, sample_order):
        """Should allow cancelling pending orders."""
        repository = OrderRepository(test_session)
        service = OrderService(repository)
        
        order = await service.cancel_order(sample_order.id)
        
        assert order.status == OrderStatus.CANCELLED.value
    
    @pytest.mark.asyncio
    async def test_cannot_cancel_delivered_order(self, test_session, sample_order):
        """Should reject cancelling delivered orders."""
        # First transition to delivered state
        sample_order.status = OrderStatus.DELIVERED.value
        await test_session.commit()
        
        repository = OrderRepository(test_session)
        service = OrderService(repository)
        
        with pytest.raises(OrderCancellationError):
            await service.cancel_order(sample_order.id)


class TestListOrders:
    """Tests for listing orders."""
    
    @pytest.mark.asyncio
    async def test_list_all_orders(self, test_session, multiple_orders):
        """Should return all orders with pagination."""
        repository = OrderRepository(test_session)
        service = OrderService(repository)
        
        orders, total = await service.list_orders(page=1, page_size=10)
        
        assert len(orders) == 5
        assert total == 5
    
    @pytest.mark.asyncio
    async def test_filter_by_user_id(self, test_session, multiple_orders):
        """Should filter orders by user_id."""
        repository = OrderRepository(test_session)
        service = OrderService(repository)
        
        orders, total = await service.list_orders(user_id=1)
        
        assert len(orders) == 3
        assert all(o.user_id == 1 for o in orders)
    
    @pytest.mark.asyncio
    async def test_filter_by_status(self, test_session, multiple_orders):
        """Should filter orders by status."""
        repository = OrderRepository(test_session)
        service = OrderService(repository)
        
        orders, total = await service.list_orders(status=OrderStatus.CONFIRMED.value)
        
        assert len(orders) == 3
        assert all(o.status == OrderStatus.CONFIRMED.value for o in orders)

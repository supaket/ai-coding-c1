"""
Order Service - Business Logic Layer
Lab 3 Complete: Extracted business logic from legacy routes.
"""

from decimal import Decimal
from typing import List, Optional, Tuple

from app.models import Order, OrderItem, OrderStatus
from app.repositories.order_repository import OrderRepository
from app.schemas import OrderCreate, OrderUpdate
from app.core.exceptions import (
    OrderNotFoundError,
    InvalidStatusTransitionError,
    OrderCancellationError,
    ProductNotFoundError,
    InsufficientStockError
)

# Mock product catalog (in real app, this would call Product Service)
PRODUCTS = {
    1: {"name": "Laptop Pro 15\"", "price": Decimal("1299.99"), "stock": 10},
    2: {"name": "Wireless Mouse", "price": Decimal("49.99"), "stock": 50},
    3: {"name": "USB-C Hub", "price": Decimal("79.99"), "stock": 30},
    4: {"name": "Mechanical Keyboard", "price": Decimal("149.99"), "stock": 20},
    5: {"name": "Monitor 27\"", "price": Decimal("449.99"), "stock": 15},
    6: {"name": "Desk Lamp", "price": Decimal("39.99"), "stock": 40},
    7: {"name": "Office Chair", "price": Decimal("299.99"), "stock": 10},
    8: {"name": "Standing Desk", "price": Decimal("599.99"), "stock": 5},
}


class OrderService:
    """Service layer for order business logic."""
    
    def __init__(self, repository: OrderRepository):
        self.repository = repository
    
    async def create_order(self, data: OrderCreate) -> Order:
        """
        Create a new order with items.
        Calculates total from product prices.
        """
        order = Order(
            user_id=data.user_id,
            shipping_address=data.shipping_address,
            notes=data.notes,
            status=OrderStatus.PENDING.value
        )
        
        total = Decimal("0.00")
        
        for item_data in data.items:
            product = PRODUCTS.get(item_data.product_id)
            if not product:
                raise ProductNotFoundError(item_data.product_id)
            
            if product["stock"] < item_data.quantity:
                raise InsufficientStockError(item_data.product_id, product["name"])
            
            # Decrement stock (mock)
            product["stock"] -= item_data.quantity
            
            product_name = product["name"]
            unit_price = product["price"]
            
            item = OrderItem(
                product_id=item_data.product_id,
                product_name=product_name,
                quantity=item_data.quantity,
                unit_price=unit_price
            )
            order.items.append(item)
            total += unit_price * item_data.quantity
        
        order.total = total
        
        return await self.repository.create(order)
    
    async def get_order(self, order_id: int) -> Order:
        """Get order by ID or raise OrderNotFoundError."""
        order = await self.repository.get_by_id(order_id)
        if not order:
            raise OrderNotFoundError(order_id)
        return order
    
    async def list_orders(
        self,
        user_id: Optional[int] = None,
        status: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[Order], int]:
        """List orders with optional filtering and pagination."""
        return await self.repository.get_all(
            user_id=user_id,
            status=status,
            page=page,
            page_size=page_size
        )
    
    async def get_user_orders(self, user_id: int) -> List[Order]:
        """Get all orders for a specific user."""
        return await self.repository.get_by_user_id(user_id)
    
    async def update_order(self, order_id: int, data: OrderUpdate) -> Order:
        """
        Update order with validation.
        Validates status transitions.
        """
        order = await self.get_order(order_id)
        
        if data.status is not None:
            new_status = OrderStatus(data.status)
            if not order.can_transition_to(new_status):
                raise InvalidStatusTransitionError(
                    order.status, 
                    data.status.value
                )
            order.status = data.status.value
        
        if data.shipping_address is not None:
            order.shipping_address = data.shipping_address
        
        if data.notes is not None:
            order.notes = data.notes
        
        return await self.repository.update(order)
    
    async def cancel_order(self, order_id: int) -> Order:
        """
        Cancel an order.
        Only allowed for certain statuses.
        """
        order = await self.get_order(order_id)
        
        if not order.can_transition_to(OrderStatus.CANCELLED):
            raise OrderCancellationError(order_id, order.status)
        
        order.status = OrderStatus.CANCELLED.value
        
        return await self.repository.update(order)

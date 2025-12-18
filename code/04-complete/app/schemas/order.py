"""
Pydantic Schemas for Order API
Lab 2 Complete: Request/response schemas with validation.
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field, ConfigDict, computed_field


class OrderStatus(str, Enum):
    """Order status enum for API."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


# ==================== Order Item Schemas ====================

class OrderItemCreate(BaseModel):
    """Request schema for creating an order item."""
    product_id: int = Field(..., gt=0, description="Product ID")
    quantity: int = Field(..., gt=0, le=100, description="Quantity (1-100)")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {"product_id": 1, "quantity": 2}
        }
    )


class OrderItemResponse(BaseModel):
    """Response schema for order item."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    product_id: int
    product_name: str
    quantity: int
    unit_price: Decimal
    
    @computed_field
    @property
    def subtotal(self) -> Decimal:
        return self.unit_price * self.quantity


# ==================== Order Schemas ====================

class OrderCreate(BaseModel):
    """Request schema for creating an order."""
    user_id: int = Field(..., gt=0, description="User ID")
    shipping_address: str | None = Field(None, max_length=500)
    notes: str | None = Field(None, max_length=1000)
    items: list[OrderItemCreate] = Field(..., min_length=1, description="Order items")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user_id": 1,
                "shipping_address": "123 Main St, City, ST 12345",
                "notes": "Leave at door",
                "items": [
                    {"product_id": 1, "quantity": 2},
                    {"product_id": 3, "quantity": 1}
                ]
            }
        }
    )


class OrderUpdate(BaseModel):
    """Request schema for updating an order."""
    status: OrderStatus | None = None
    shipping_address: str | None = Field(None, max_length=500)
    notes: str | None = Field(None, max_length=1000)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {"status": "confirmed"}
        }
    )


class OrderResponse(BaseModel):
    """Response schema for order with items."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    status: str
    total: Decimal
    shipping_address: str | None
    notes: str | None
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemResponse]
    
    @computed_field
    @property
    def item_count(self) -> int:
        return len(self.items)


class OrderSummary(BaseModel):
    """Response schema for order list (without items)."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    status: str
    total: Decimal
    created_at: datetime


# ==================== Pagination Schemas ====================

class PaginatedOrders(BaseModel):
    """Paginated order list response."""
    items: list[OrderSummary]
    total: int
    page: int
    page_size: int
    
    @computed_field
    @property
    def total_pages(self) -> int:
        return (self.total + self.page_size - 1) // self.page_size


# ==================== Error Schemas ====================

class ErrorResponse(BaseModel):
    """Error response schema."""
    error: str
    detail: str | None = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {"error": "Order not found", "detail": "Order with ID 999 does not exist"}
        }
    )

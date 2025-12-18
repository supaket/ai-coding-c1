"""
Pydantic Schemas for Product API
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, computed_field


class ProductCreate(BaseModel):
    """Request schema for creating a product."""
    name: str = Field(..., min_length=1, max_length=200, description="Product name")
    description: Optional[str] = Field(None, max_length=2000, description="Product description")
    price: Decimal = Field(..., gt=0, description="Product price")
    stock: int = Field(0, ge=0, description="Initial stock quantity")
    category: Optional[str] = Field(None, max_length=50, description="Product category")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Laptop Pro 15",
                "description": "High-performance laptop",
                "price": "1299.99",
                "stock": 50,
                "category": "electronics"
            }
        }
    )


class ProductResponse(BaseModel):
    """Response schema for product."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str]
    price: Decimal
    stock: int
    category: Optional[str]
    created_at: datetime

    @computed_field
    @property
    def is_low_stock(self) -> bool:
        """Check if product is low on stock."""
        return self.stock < 10


class ProductStockUpdate(BaseModel):
    """Request schema for updating product stock."""
    stock: int = Field(..., ge=0, description="New stock quantity")


class LowStockItem(BaseModel):
    """Response schema for low stock items."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    stock: int
    category: Optional[str]


class BulkRestockItem(BaseModel):
    """Single item in bulk restock request."""
    product_id: int = Field(..., gt=0, description="Product ID")
    quantity: int = Field(..., gt=0, description="Quantity to add")


class BulkRestockRequest(BaseModel):
    """Request schema for bulk restock."""
    items: list[BulkRestockItem] = Field(..., min_length=1, description="Items to restock")


class BulkRestockResponse(BaseModel):
    """Response schema for bulk restock."""
    updated_count: int
    items: list[ProductResponse]

"""
Order Model - SQLAlchemy 2.0 Mapped Syntax
Lab 2 Complete: Converted from legacy Flask model.
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional
from sqlalchemy import String, Numeric, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class OrderStatus(str, Enum):
    """Valid order statuses with transition rules."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    
    @classmethod
    def valid_transitions(cls):
        return {
            cls.PENDING: [cls.CONFIRMED, cls.CANCELLED],
            cls.CONFIRMED: [cls.PROCESSING, cls.CANCELLED],
            cls.PROCESSING: [cls.SHIPPED, cls.CANCELLED],
            cls.SHIPPED: [cls.DELIVERED],
            cls.DELIVERED: [],
            cls.CANCELLED: []
        }


class Order(Base):
    """Order model - migrated from legacy Flask app."""
    
    __tablename__ = "orders"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(index=True)
    status: Mapped[str] = mapped_column(String(20), default=OrderStatus.PENDING.value)
    total: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"))
    shipping_address: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    
    items: Mapped[List["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    
    __table_args__ = (
        Index("idx_user_status", "user_id", "status"),
        Index("idx_created_at", "created_at"),
    )
    
    def can_transition_to(self, new_status: OrderStatus) -> bool:
        """Check if status transition is valid."""
        current = OrderStatus(self.status)
        valid = OrderStatus.valid_transitions().get(current, [])
        return new_status in valid


# Import at bottom to avoid circular imports
from app.models.order_item import OrderItem

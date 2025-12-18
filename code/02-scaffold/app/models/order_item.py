"""
OrderItem Model - SQLAlchemy 2.0 Mapped Syntax
Lab 2 Complete: Order line items.
"""

from decimal import Decimal
from sqlalchemy import String, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class OrderItem(Base):
    """Order line item model."""
    
    __tablename__ = "order_items"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(index=True)
    product_name: Mapped[str] = mapped_column(String(200))
    quantity: Mapped[int]
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    
    order: Mapped["Order"] = relationship("Order", back_populates="items")
    
    @property
    def subtotal(self) -> Decimal:
        """Calculate line item subtotal."""
        return Decimal(str(self.unit_price)) * self.quantity


from app.models.order import Order

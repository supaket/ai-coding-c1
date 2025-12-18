"""
Product Model - SQLAlchemy 2.0 Mapped Syntax
"""

from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import String, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Product(Base):
    """Product catalog model."""
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    stock: Mapped[int] = mapped_column(default=0)
    category: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    @property
    def is_low_stock(self) -> bool:
        """Check if product is low on stock (threshold: 10)."""
        return self.stock < 10

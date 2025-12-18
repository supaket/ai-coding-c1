"""
User Model - SQLAlchemy 2.0 Mapped Syntax
"""

from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.order import Order


class User(Base):
    """User model for authentication and profiles."""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Relationships
    orders: Mapped[List["Order"]] = relationship(
        "Order",
        back_populates="user",
        lazy="selectin"
    )

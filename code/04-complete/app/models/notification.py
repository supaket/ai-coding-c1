"""
Notification Model - SQLAlchemy 2.0 Mapped Syntax
"""

from datetime import UTC, datetime
from enum import Enum

from sqlalchemy import String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class NotificationType(str, Enum):
    """Notification types."""
    ORDER_CREATED = "order_created"
    ORDER_SHIPPED = "order_shipped"
    ORDER_DELIVERED = "order_delivered"
    ORDER_CANCELLED = "order_cancelled"
    LOW_STOCK = "low_stock"
    RESTOCK = "restock"


class NotificationStatus(str, Enum):
    """Notification status."""
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"


class Notification(Base):
    """Notification model for tracking messages."""
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(50))
    recipient_id: Mapped[int] = mapped_column(index=True)
    subject: Mapped[str] = mapped_column(String(200))
    message: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(
        String(20),
        default=NotificationStatus.PENDING.value,
        index=True
    )
    reference_id: Mapped[int | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
    sent_at: Mapped[datetime | None] = mapped_column(nullable=True)

    __table_args__ = (
        Index("idx_notification_status_created", "status", "created_at"),
    )

"""Notification Service - Business Logic Layer."""

from datetime import datetime

from app.models import Notification, NotificationType, NotificationStatus
from app.repositories.notification_repository import NotificationRepository
from app.core.exceptions import NotificationNotFoundError


class NotificationService:
    """Service layer for notification business logic."""

    def __init__(self, repository: NotificationRepository) -> None:
        self.repository = repository

    async def get_pending_notifications(self) -> list[Notification]:
        """Get all pending notifications."""
        return await self.repository.get_pending()

    async def mark_as_sent(
        self,
        notification_id: int,
        sent_at: datetime | None = None,
    ) -> Notification:
        """Mark notification as sent."""
        notification = await self.repository.mark_sent(notification_id, sent_at)
        if not notification:
            raise NotificationNotFoundError(notification_id)
        return notification

    async def create_order_notification(
        self,
        notification_type: NotificationType,
        recipient_id: int,
        order_id: int,
        message: str
    ) -> Notification:
        """Create a notification for order events."""
        subject_map = {
            NotificationType.ORDER_CREATED: "Order Created",
            NotificationType.ORDER_SHIPPED: "Order Shipped",
            NotificationType.ORDER_DELIVERED: "Order Delivered",
            NotificationType.ORDER_CANCELLED: "Order Cancelled",
        }
        
        notification = Notification(
            type=notification_type.value,
            recipient_id=recipient_id,
            subject=subject_map.get(notification_type, "Order Update"),
            message=message,
            reference_id=order_id
        )
        return await self.repository.create(notification)

    async def create_low_stock_notification(
        self,
        product_id: int,
        product_name: str,
        current_stock: int
    ) -> Notification:
        """Create a low stock notification."""
        notification = Notification(
            type=NotificationType.LOW_STOCK.value,
            recipient_id=0,  # Admin notification
            subject=f"Low Stock Alert: {product_name}",
            message=f"Product '{product_name}' has low stock: {current_stock} units remaining",
            reference_id=product_id
        )
        return await self.repository.create(notification)

"""
Notification Repository - Data Access Layer
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Notification, NotificationStatus


class NotificationRepository:
    """Repository for Notification database operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, notification: Notification) -> Notification:
        """Create a new notification."""
        self.session.add(notification)
        await self.session.commit()
        await self.session.refresh(notification)
        return notification

    async def get_by_id(self, notification_id: int) -> Optional[Notification]:
        """Get notification by ID."""
        query = select(Notification).where(Notification.id == notification_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_pending(self) -> List[Notification]:
        """Get all pending notifications."""
        query = (
            select(Notification)
            .where(Notification.status == NotificationStatus.PENDING.value)
            .order_by(Notification.created_at)
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def mark_sent(
        self,
        notification_id: int,
        sent_at: Optional[datetime] = None
    ) -> Optional[Notification]:
        """Mark notification as sent."""
        notification = await self.get_by_id(notification_id)
        if notification:
            notification.status = NotificationStatus.SENT.value
            notification.sent_at = sent_at or datetime.utcnow()
            await self.session.commit()
            await self.session.refresh(notification)
        return notification

    async def create_bulk(self, notifications: List[Notification]) -> List[Notification]:
        """Create multiple notifications."""
        self.session.add_all(notifications)
        await self.session.commit()
        for notification in notifications:
            await self.session.refresh(notification)
        return notifications

"""
Pydantic Schemas for Notification API
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NotificationResponse(BaseModel):
    """Response schema for notification."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    type: str
    recipient_id: int
    subject: str
    message: str
    status: str
    reference_id: int | None
    created_at: datetime
    sent_at: datetime | None


class NotificationMarkSent(BaseModel):
    """Request schema for marking notification as sent."""
    sent_at: datetime | None = Field(None, description="When the notification was sent")


class PendingNotificationsResponse(BaseModel):
    """Response schema for pending notifications."""
    items: list[NotificationResponse]
    total: int

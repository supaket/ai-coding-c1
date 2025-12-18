"""
Notifications API Endpoints
"""

from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.exceptions import NotificationNotFoundError
from app.repositories.notification_repository import NotificationRepository
from app.services.notification_service import NotificationService
from app.schemas import (
    NotificationResponse,
    NotificationMarkSent,
    PendingNotificationsResponse,
    ErrorResponse,
)

router = APIRouter()


def get_notification_service(
    session: AsyncSession = Depends(get_async_session)
) -> NotificationService:
    """Dependency to get NotificationService instance."""
    repository = NotificationRepository(session)
    return NotificationService(repository)


@router.get(
    "/notifications/pending",
    response_model=PendingNotificationsResponse
)
async def get_pending_notifications(
    service: NotificationService = Depends(get_notification_service)
):
    """Get all pending notifications."""
    notifications = await service.get_pending_notifications()
    return PendingNotificationsResponse(
        items=notifications,
        total=len(notifications)
    )


@router.put(
    "/notifications/{notification_id}/sent",
    response_model=NotificationResponse,
    responses={404: {"model": ErrorResponse}}
)
async def mark_notification_sent(
    notification_id: int,
    data: Optional[NotificationMarkSent] = None,
    service: NotificationService = Depends(get_notification_service)
):
    """Mark a notification as sent."""
    try:
        sent_at = data.sent_at if data else None
        notification = await service.mark_as_sent(notification_id, sent_at)
        return notification
    except NotificationNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

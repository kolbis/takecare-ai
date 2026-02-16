"""Notify caregiver (WhatsApp/email/SMS). Mock: log only."""
import logging
from typing import Any

logger = logging.getLogger(__name__)


class CaregiverNotificationService:
    """Mock: log only. Replace with real channel for production."""

    def notify(
        self,
        user_id: str,
        caregiver_id: str,
        reason: str,
        summary: str,
        contact_phone: str | None = None,
        contact_email: str | None = None,
    ) -> dict[str, Any]:
        logger.info(
            "CaregiverNotificationService.notify (mocked): user_id=%s caregiver_id=%s reason=%s summary=%s",
            user_id, caregiver_id, reason, summary[:100],
        )
        return {"sent": True, "mocked": True}


def get_caregiver_notification_service() -> CaregiverNotificationService:
    return CaregiverNotificationService()

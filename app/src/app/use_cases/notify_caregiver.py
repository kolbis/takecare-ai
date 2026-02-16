"""Notify caregiver (escalation). Mock: log only."""
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class NotifyCaregiverInput:
    user_id: str
    reason: str
    summary: str
    severity: str | None = None


@dataclass
class NotifyCaregiverResult:
    success: bool


class NotifyCaregiver:
    """Mock: log only; no real WhatsApp/email."""

    def execute(self, input: NotifyCaregiverInput) -> NotifyCaregiverResult:
        logger.info(
            "NotifyCaregiver (mocked): user_id=%s reason=%s summary=%s",
            input.user_id,
            input.reason,
            input.summary[:100] if len(input.summary) > 100 else input.summary,
        )
        return NotifyCaregiverResult(success=True)

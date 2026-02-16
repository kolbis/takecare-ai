"""Snooze current reminder."""
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class SnoozeDoseInput:
    user_id: str
    reminder_id: str
    snooze_minutes: int = 15


@dataclass
class SnoozeDoseResult:
    success: bool
    snooze_until: Optional[datetime] = None


class SnoozeDose:
    """Mock: no real scheduler; just returns success and snooze_until."""

    def execute(self, input: SnoozeDoseInput) -> SnoozeDoseResult:
        snooze_until = datetime.utcnow() + timedelta(minutes=input.snooze_minutes)
        return SnoozeDoseResult(success=True, snooze_until=snooze_until)

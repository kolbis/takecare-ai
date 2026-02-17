"""Snooze current reminder (one or more events via reminder_ids)."""
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import List


@dataclass
class SnoozeDoseInput:
    user_id: str
    reminder_ids: List[str]
    snooze_minutes: int = 15


@dataclass
class SnoozeDoseResult:
    success: bool
    snooze_until: datetime | None = None


class SnoozeDose:
    """Mock: no real scheduler; just returns success and snooze_until."""

    def execute(self, input: SnoozeDoseInput) -> SnoozeDoseResult:
        if not input.reminder_ids:
            return SnoozeDoseResult(success=False, snooze_until=None)
        snooze_until = datetime.now(timezone.utc) + timedelta(minutes=input.snooze_minutes)
        return SnoozeDoseResult(success=True, snooze_until=snooze_until)

"""Dose event repository interface and mock."""
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List

from app.domain.entities import DoseEvent


class DoseEventRepository(ABC):
    @abstractmethod
    def add(self, event: DoseEvent) -> None:
        ...

    @abstractmethod
    def get_recent_doses(
        self,
        user_id: str,
        medication_id: str,
        slot_time: str,
        within_hours: float = 24.0,
    ) -> List[DoseEvent]:
        """Doses already recorded for this medication/slot in the time window."""
        ...


class MockDoseEventRepository(DoseEventRepository):
    """Mock: in-memory list; get_recent_doses returns empty by default (SAFE)."""

    def __init__(self, recent_doses: List[DoseEvent] | None = None):
        self._events: List[DoseEvent] = list(recent_doses or [])

    def add(self, event: DoseEvent) -> None:
        self._events.append(event)

    def get_recent_doses(
        self,
        user_id: str,
        medication_id: str,
        slot_time: str,
        within_hours: float = 24.0,
    ) -> List[DoseEvent]:
        cutoff = datetime.utcnow() - timedelta(hours=within_hours)
        return [
            e
            for e in self._events
            if e.user_id == user_id
            and e.medication_id == medication_id
            and e.slot_time == slot_time
            and e.occurred_at >= cutoff
        ]

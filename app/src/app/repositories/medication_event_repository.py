"""Medication event (reminder) repository interface and mock."""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from app.domain.entities import MedicationEvent


class MedicationEventRepository(ABC):
    @abstractmethod
    def get_by_id(self, event_id: str) -> Optional[MedicationEvent]:
        ...

    @abstractmethod
    def get_current_for_user(self, user_id: str) -> Optional[MedicationEvent]:
        """Get current pending reminder for user (e.g. the one we just sent)."""
        ...

    @abstractmethod
    def list_pending_for_user(self, user_id: str) -> List[MedicationEvent]:
        ...


class MockMedicationEventRepository(MedicationEventRepository):
    """Mock: returns a fixed current reminder."""

    def __init__(self):
        self._event = MedicationEvent(
            id="rem1",
            user_id="u1",
            medication_id="med1",
            medication_name="Aspirin",
            slot_time="08:00",
            dose_index=0,
            scheduled_at=datetime.utcnow(),
            status="pending",
        )

    def get_by_id(self, event_id: str) -> Optional[MedicationEvent]:
        return self._event if event_id == self._event.id else self._event

    def get_current_for_user(self, user_id: str) -> Optional[MedicationEvent]:
        return self._event

    def list_pending_for_user(self, user_id: str) -> List[MedicationEvent]:
        return [self._event]

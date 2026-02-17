"""Medication event (reminder) repository interface and mock."""
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import List, Optional

from app.domain.entities import MedicationEvent
from app.domain.value_objects import MedicationEventStatus


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

    @abstractmethod
    def get_current_slot_events_for_user(self, user_id: str) -> List[MedicationEvent]:
        """Return all pending events for the user that belong to the current reminder slot (same slot_time)."""
        ...


class MockMedicationEventRepository(MedicationEventRepository):
    """Mock: returns a fixed current reminder; slot can have multiple events."""

    def __init__(self):
        self._event = MedicationEvent(
            id="rem1",
            user_id="u1",
            medication_id="med1",
            medication_name="Aspirin",
            slot_time="08:00",
            dose_index=0,
            scheduled_at=datetime.now(timezone.utc),
            status=MedicationEventStatus.PENDING,
        )
        self._slot_events = [
            self._event,
            MedicationEvent(
                id="rem2",
                user_id="u1",
                medication_id="med2",
                medication_name="Ibuprofen",
                slot_time="08:00",
                dose_index=0,
                scheduled_at=datetime.now(timezone.utc),
                status=MedicationEventStatus.PENDING,
            ),
            MedicationEvent(
                id="rem3",
                user_id="u1",
                medication_id="med3",
                medication_name="Vitamin D",
                slot_time="08:00",
                dose_index=0,
                scheduled_at=datetime.now(timezone.utc),
                status=MedicationEventStatus.PENDING,
            ),
        ]

    def get_by_id(self, event_id: str) -> Optional[MedicationEvent]:
        return self._event if event_id == self._event.id else self._event

    def get_current_for_user(self, user_id: str) -> Optional[MedicationEvent]:
        return self._event

    def list_pending_for_user(self, user_id: str) -> List[MedicationEvent]:
        return [self._event]

    def get_current_slot_events_for_user(self, user_id: str) -> List[MedicationEvent]:
        return self._slot_events

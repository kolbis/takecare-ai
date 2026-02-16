"""Get medication event (reminder) by id or current for user."""
from dataclasses import dataclass
from typing import Optional

from app.domain.entities import MedicationEvent
from app.repositories.medication_event_repository import MedicationEventRepository


@dataclass
class GetMedicationEventResult:
    event: Optional[MedicationEvent]


class GetMedicationEvent:
    def __init__(self, medication_event_repository: MedicationEventRepository):
        self._repo = medication_event_repository

    def execute_by_id(self, event_id: str) -> GetMedicationEventResult:
        event = self._repo.get_by_id(event_id)
        return GetMedicationEventResult(event=event)

    def execute_current_for_user(self, user_id: str) -> GetMedicationEventResult:
        event = self._repo.get_current_for_user(user_id)
        return GetMedicationEventResult(event=event)

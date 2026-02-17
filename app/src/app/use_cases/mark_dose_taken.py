"""Mark dose as taken."""
from dataclasses import dataclass
from datetime import datetime

from app.domain.events import DoseEvent, DoseEventSource
from app.repositories.dose_event_repository import DoseEventRepository
from app.repositories.medication_event_repository import MedicationEventRepository


@dataclass
class MarkDoseTakenInput:
    user_id: str
    medication_id: str
    slot_time: str
    dose_index: int
    source: DoseEventSource = "user_confirmed"


@dataclass
class MarkDoseTakenResult:
    success: bool
    event_id: str | None = None


class MarkDoseTaken:
    def __init__(
        self,
        dose_event_repository: DoseEventRepository,
        medication_event_repository: MedicationEventRepository,
    ):
        self._dose_repo = dose_event_repository
        self._med_event_repo = medication_event_repository

    def execute(self, input: MarkDoseTakenInput) -> MarkDoseTakenResult:
        event = DoseEvent(
            id=f"dose-{datetime.utcnow().timestamp()}",
            user_id=input.user_id,
            medication_id=input.medication_id,
            slot_time=input.slot_time,
            dose_index=input.dose_index,
            occurred_at=datetime.utcnow(),
            source=input.source,
        )
        self._dose_repo.add(event)
        return MarkDoseTakenResult(success=True, event_id=event.id)

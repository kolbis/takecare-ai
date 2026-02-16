"""Simple container: wires mock repositories and use cases."""
from datetime import date

from app.repositories import (
    MockUserRepository,
    MockScheduleRepository,
    MockMedicationEventRepository,
    MockDoseEventRepository,
    MockCaregiverRepository,
)
from app.use_cases import (
    GetUserByPhone,
    GetScheduleForUser,
    GetMedicationEvent,
    MarkDoseTaken,
    SnoozeDose,
    NotifyCaregiver,
    CheckDoubleDoseRisk,
    CheckSymptomSeverity,
)
from app.rag import MedicationRAG


class Container:
    """Holds repositories and use cases. Use this from api/agentic."""

    def __init__(self):
        self._user_repo = MockUserRepository()
        self._schedule_repo = MockScheduleRepository()
        self._med_event_repo = MockMedicationEventRepository()
        self._dose_repo = MockDoseEventRepository()
        self._caregiver_repo = MockCaregiverRepository()
        self._rag = MedicationRAG()

        self.get_user_by_phone = GetUserByPhone(self._user_repo)
        self.get_schedule = GetScheduleForUser(self._schedule_repo)
        self.get_medication_event = GetMedicationEvent(self._med_event_repo)
        self.mark_dose_taken = MarkDoseTaken(
            self._dose_repo,
            self._med_event_repo,
        )
        self.snooze_dose = SnoozeDose()
        self.notify_caregiver = NotifyCaregiver()
        self.check_double_dose_risk = CheckDoubleDoseRisk(self._dose_repo)
        self.check_symptom_severity = CheckSymptomSeverity()

    @property
    def rag(self) -> MedicationRAG:
        return self._rag


_default_container: Container | None = None


def get_container() -> Container:
    global _default_container
    if _default_container is None:
        _default_container = Container()
    return _default_container

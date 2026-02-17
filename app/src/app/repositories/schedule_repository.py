from abc import ABC, abstractmethod
from datetime import date
from typing import List

from app.domain.entities import UserMedicationEntity
from app.domain.value_objects import (
    MedicationId,
    MedicationName,
    UserId,
    UserMedicationId,
)
from .medication_repository import MOCK_MEDICATION_ID
from .mock import MOCK_USER_MEDICATION_ID


class ScheduleRepository(ABC):
    @abstractmethod
    def get_schedule(
        self, user_id: str, for_date: date
    ) -> List[UserMedicationEntity]: ...


class MockScheduleRepository(ScheduleRepository):
    """Mock: returns one assigned medication with two slots for today."""

    def get_schedule(self, user_id: str, for_date: date) -> List[UserMedicationEntity]:
        return [
            UserMedicationEntity(
                id=UserMedicationId.from_str(MOCK_USER_MEDICATION_ID),
                user_id=UserId.from_str(user_id),
                medication_id=MedicationId.from_str(MOCK_MEDICATION_ID),
                name=MedicationName("Aspirin"),
                slots=["08:00", "20:00"],
            )
        ]

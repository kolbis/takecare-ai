"""Schedule repository interface and mock."""
from abc import ABC, abstractmethod
from datetime import date
from typing import List

from app.domain.entities import UserMedication


class ScheduleRepository(ABC):
    @abstractmethod
    def get_schedule(self, user_id: str, for_date: date) -> List[UserMedication]:
        ...


class MockScheduleRepository(ScheduleRepository):
    """Mock: returns one assigned medication with two slots for today."""

    def get_schedule(self, user_id: str, for_date: date) -> List[UserMedication]:
        return [
            UserMedication(
                id="med1",
                user_id=user_id,
                medication_id="med1",
                name="Aspirin",
                slots=["08:00", "20:00"],
            )
        ]

"""Schedule repository interface and mock."""
from abc import ABC, abstractmethod
from datetime import date
from typing import List

from app.domain.entities import Medication


class ScheduleRepository(ABC):
    @abstractmethod
    def get_schedule(self, user_id: str, for_date: date) -> List[Medication]:
        ...


class MockScheduleRepository(ScheduleRepository):
    """Mock: returns one medication with two slots for today."""

    def get_schedule(self, user_id: str, for_date: date) -> List[Medication]:
        return [
            Medication(
                id="med1",
                user_id=user_id,
                name="Aspirin",
                slots=["08:00", "20:00"],
            )
        ]

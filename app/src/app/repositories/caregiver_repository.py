"""Caregiver repository interface and mock."""
from abc import ABC, abstractmethod
from typing import List

from app.domain.entities import Caregiver


class CaregiverRepository(ABC):
    @abstractmethod
    def get_caregivers_for_user(self, user_id: str) -> List[Caregiver]:
        ...


class MockCaregiverRepository(CaregiverRepository):
    """Mock: returns a fixed list of caregivers for user."""

    def __init__(self):
        self._caregivers = [
            Caregiver(
                id="c1",
                contact_phone="+0987654321",
                contact_email="caregiver@example.com",
            )
        ]

    def get_caregivers_for_user(self, user_id: str) -> List[Caregiver]:
        return self._caregivers

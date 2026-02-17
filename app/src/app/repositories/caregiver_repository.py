from abc import ABC, abstractmethod
from typing import List

from app.domain.entities import CaregiverEntity
from app.domain.value_objects import CaregiverId, Email, Phone
from .mock import MOCK_CAREGIVER_ID


class CaregiverRepository(ABC):
    @abstractmethod
    def get_caregivers_for_user(self, user_id: str) -> List[CaregiverEntity]: ...


class MockCaregiverRepository(CaregiverRepository):
    """Mock: returns a fixed list of caregivers for user."""

    def __init__(self):
        self._caregivers = [
            CaregiverEntity(
                id=CaregiverId.from_str(MOCK_CAREGIVER_ID),
                contact_phone=Phone("+0987654321"),
                contact_email=Email("caregiver@example.com"),
                for_user_ids=[],
            )
        ]

    def get_caregivers_for_user(self, user_id: str) -> List[CaregiverEntity]:
        return self._caregivers

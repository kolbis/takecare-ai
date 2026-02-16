"""Caregiver link repository interface and mock."""
from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities import CaregiverLink


class CaregiverRepository(ABC):
    @abstractmethod
    def get_by_user_id(self, user_id: str) -> Optional[CaregiverLink]:
        ...


class MockCaregiverRepository(CaregiverRepository):
    """Mock: returns a fixed caregiver link."""

    def __init__(self):
        self._link = CaregiverLink(
            user_id="u1",
            caregiver_id="c1",
            contact_phone="+0987654321",
            contact_email="caregiver@example.com",
        )

    def get_by_user_id(self, user_id: str) -> Optional[CaregiverLink]:
        return self._link

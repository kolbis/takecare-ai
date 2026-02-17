from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities import MedicationEntity
from app.domain.value_objects import (
    MedicationDescription,
    MedicationId,
    MedicationName,
)
from .mock import MOCK_MEDICATION_ID


class MedicationRepository(ABC):
    @abstractmethod
    def get_by_id(self, medication_id: str) -> Optional[MedicationEntity]:
        """Return the medication from the catalog by id."""
        ...

    @abstractmethod
    def list_all(self) -> List[MedicationEntity]:
        """Return all medications in the catalog."""
        ...


class MockMedicationRepository(MedicationRepository):
    """Mock: returns a fixed catalog with one medication."""

    def __init__(self):
        self._medications: List[MedicationEntity] = [
            MedicationEntity(
                id=MedicationId.from_str(MOCK_MEDICATION_ID),
                name=MedicationName("Aspirin"),
                description=MedicationDescription(
                    "Pain reliever and fever reducer. Take with food or water."
                ),
                warnings=["Do not exceed recommended dose."],
                side_effects=[],
                interactions=[],
                precautions=[],
                how_to_take=[],
                how_to_store=[],
            )
        ]

    def get_by_id(self, medication_id: str) -> Optional[MedicationEntity]:
        for m in self._medications:
            if str(m.id) == medication_id:
                return m
        return None

    def list_all(self) -> List[MedicationEntity]:
        return list(self._medications)

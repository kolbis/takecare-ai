"""Value objects (immutable)."""
from dataclasses import dataclass
from datetime import time
from typing import Literal


@dataclass(frozen=True)
class MedicationSlot:
    """A scheduled slot for a medication (e.g. 08:00)."""
    time: time
    dose_index: int


@dataclass(frozen=True)
class ReminderContext:
    """Context for the current reminder (which medication, which slot)."""
    medication_id: str
    medication_name: str
    slot_time: time
    dose_index: int
    reminder_id: str


Language = Literal["en", "he"]
DoubleDoseStatus = Literal["SAFE", "RISK"]
SymptomSeverity = Literal["low", "medium", "high", "emergency"]

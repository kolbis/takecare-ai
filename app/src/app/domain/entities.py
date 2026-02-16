"""Domain entities."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.domain.value_objects import Language


@dataclass
class User:
    id: str
    phone: str
    language: Language
    caregiver_id: Optional[str]
    timezone: str
    name: Optional[str] = None


@dataclass
class Medication:
    id: str
    user_id: str
    name: str
    slots: list[str]  # e.g. ["08:00", "20:00"]


@dataclass
class MedicationEvent:
    """A reminder event (scheduled slot)."""
    id: str
    user_id: str
    medication_id: str
    medication_name: str
    slot_time: str  # "08:00"
    dose_index: int
    scheduled_at: datetime
    status: str  # "pending", "snoozed", "taken", "missed"


@dataclass
class DoseEvent:
    """Record of a dose taken (or missed, etc.)."""
    id: str
    user_id: str
    medication_id: str
    slot_time: str
    dose_index: int
    occurred_at: datetime
    source: str  # "user_confirmed", "snooze", "missed", "escalated"


@dataclass
class CaregiverLink:
    user_id: str
    caregiver_id: str
    contact_phone: Optional[str]
    contact_email: Optional[str]

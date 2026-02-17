from dataclasses import dataclass
from datetime import datetime
from typing import Literal

MedicationEventStatus = Literal["pending", "snoozed", "taken", "missed"]

@dataclass
class MedicationEvent:
    id: str
    user_id: str
    medication_id: str
    medication_name: str
    # TODO: do we need slot_time? why not using datetime or schedule_at?
    slot_time: str  # "08:00"
    dose_index: int  # Index of this dose in the medication schedule (e.g. 0=first slot, 1=second slot).
    scheduled_at: datetime
    status: MedicationEventStatus


from dataclasses import dataclass
from datetime import datetime
from typing import Literal

DoseEventSource = Literal["user_confirmed", "snooze", "missed", "escalated"]


@dataclass
class DoseEvent:
    id: str
    user_id: str
    medication_id: str
    slot_time: str
    dose_index: int
    occurred_at: datetime
    source: DoseEventSource

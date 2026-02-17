from dataclasses import dataclass
from app.domain import value_objects


@dataclass
class UserMedicationEntity:
    id: value_objects.UserMedicationId
    user_id: value_objects.UserId
    medication_id: value_objects.MedicationId
    name: value_objects.MedicationName
    slots: list[str]  # e.g. ["08:00", "20:00"]

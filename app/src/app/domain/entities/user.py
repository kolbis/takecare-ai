from dataclasses import dataclass
from app.domain import value_objects
from app.domain.entities import UserMedicationEntity


@dataclass
class UserEntity:
    id: value_objects.UserId
    phone: value_objects.Phone
    language: value_objects.Language
    timezone: value_objects.Timezone
    first_name: value_objects.FirstName
    last_name: value_objects.LastName
    date_of_birth: value_objects.DateOfBirth
    caregiver_ids: list[value_objects.CaregiverId] | None = None
    medications: list["UserMedicationEntity"] | None = None

    def __post_init__(self) -> None:
        if self.medications is None:
            object.__setattr__(self, "medications", [])
        if self.caregiver_ids is None:
            object.__setattr__(self, "caregiver_ids", [])
    
    def add_caregiver(self, caregiver_id: value_objects.CaregiverId) -> None:
        if caregiver_id not in self.caregiver_ids:
            self.caregiver_ids.append(caregiver_id)
    
    def remove_caregiver(self, caregiver_id: value_objects.CaregiverId) -> None:
        if caregiver_id in self.caregiver_ids:
            self.caregiver_ids.remove(caregiver_id)

    def add_medication(self, medication: UserMedicationEntity) -> None:
        if medication not in self.medications:
            self.medications.append(medication)
    
    def remove_medication(self, medication: UserMedicationEntity) -> None:
        if medication in self.medications:
            self.medications.remove(medication)

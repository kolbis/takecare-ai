from dataclasses import dataclass, field
from app.domain import value_objects


@dataclass
class CaregiverEntity:
    id: value_objects.CaregiverId
    contact_phone: value_objects.Phone | None = None
    contact_email: value_objects.Email | None = None
    for_user_ids: list[value_objects.UserId] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        if self.contact_phone is None and self.contact_email is None:
            raise ValueError("Either contact_phone or contact_email must be set")
        if self.for_user_ids is None:
            object.__setattr__(self, "for_user_ids", [])

    def add_for_user(self, user_id: value_objects.UserId) -> None:
        if user_id not in self.for_user_ids:
            self.for_user_ids.append(user_id)
    
    def remove_for_user(self, user_id: value_objects.UserId) -> None:
        if user_id in self.for_user_ids:
            self.for_user_ids.remove(user_id)


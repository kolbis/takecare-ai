from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class UserMedicationId:
    value: UUID

    def __post_init__(self) -> None:
        if not isinstance(self.value, UUID):
            raise TypeError("UserMedicationId must be a UUID instance.")

    @classmethod
    def new(cls) -> "UserMedicationId":
        return cls(uuid4())

    @classmethod
    def from_str(cls, raw: str) -> "UserMedicationId":
        try:
            return cls(UUID(raw))
        except ValueError:
            raise ValueError(f"Invalid UUID string: {raw}")

    def __str__(self) -> str:
        return str(self.value)

from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class CaregiverId:
    value: UUID

    def __post_init__(self) -> None:
        if not isinstance(self.value, UUID):
            raise TypeError("CaregiverId must be a UUID instance.")

    @classmethod
    def new(cls) -> "CaregiverId":
        return cls(uuid4())

    @classmethod
    def from_str(cls, raw: str) -> "CaregiverId":
        try:
            return cls(UUID(raw))
        except ValueError:
            raise ValueError(f"Invalid UUID string: {raw}")

    def __str__(self) -> str:
        return str(self.value)

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MedicationName:
    value: str

    MAX_LENGTH = 200

    def __post_init__(self) -> None:
        normalized = self.value.strip()

        if not normalized:
            raise ValueError("Medication name cannot be empty.")

        if len(normalized) > self.MAX_LENGTH:
            raise ValueError("Medication name is too long.")

        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value

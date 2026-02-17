from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MedicationDescription:
    value: str

    MAX_LENGTH = 5000

    def __post_init__(self) -> None:
        normalized = self.value.strip()

        if not normalized:
            raise ValueError("Medication description cannot be empty.")

        if len(normalized) > self.MAX_LENGTH:
            raise ValueError("Medication description is too long.")

        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value

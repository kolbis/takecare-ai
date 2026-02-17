from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FirstName:
    value: str

    def __post_init__(self) -> None:
        normalized = self._normalize(self.value)

        if not normalized:
            raise ValueError("First name cannot be empty.")

        if len(normalized) > 100:
            raise ValueError("First name is too long.")

        object.__setattr__(self, "value", normalized)

    @staticmethod
    def _normalize(raw: str) -> str:
        return raw.strip()

    def __str__(self) -> str:
        return self.value

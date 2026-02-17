from dataclasses import dataclass
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


@dataclass(frozen=True, slots=True)
class Timezone:
    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()

        if not normalized:
            raise ValueError("Timezone cannot be empty.")

        try:
            # Validate against real IANA database
            ZoneInfo(normalized)
        except ZoneInfoNotFoundError:
            raise ValueError(f"Invalid timezone: {normalized}")

        object.__setattr__(self, "value", normalized)

    def to_zoneinfo(self) -> ZoneInfo:
        return ZoneInfo(self.value)

    def __str__(self) -> str:
        return self.value

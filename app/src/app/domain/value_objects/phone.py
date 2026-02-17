from dataclasses import dataclass
import re

_E164_REGEX = re.compile(r"^\+[1-9]\d{1,14}$")


@dataclass(frozen=True, slots=True)
class Phone:
    value: str

    def __post_init__(self) -> None:
        normalized = self._normalize(self.value)

        if not _E164_REGEX.match(normalized):
            raise ValueError("Phone number must be in E.164 format, e.g. +14155552671")

        object.__setattr__(self, "value", normalized)

    @staticmethod
    def _normalize(raw: str) -> str:
        # Remove spaces, dashes, parentheses
        cleaned = re.sub(r"[^\d+]", "", raw.strip())
        return cleaned

    def __str__(self) -> str:
        return self.value

from dataclasses import dataclass
import re

_EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$"
)


@dataclass(frozen=True, slots=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()

        if not normalized:
            raise ValueError("Email cannot be empty.")

        if not _EMAIL_REGEX.match(normalized):
            raise ValueError(f"Invalid email address: {self.value}")

        # Because frozen=True
        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value

from dataclasses import dataclass
import re

_LANGUAGE_CODE_REGEX = re.compile(r"^[a-z]{2}$")

_SUPPORTED_LANGUAGES = {
    "en": "English",
    "he": "Hebrew",
}


@dataclass(frozen=True, slots=True)
class Language:
    code: str

    def __post_init__(self) -> None:
        normalized = self.code.strip().lower()

        if not _LANGUAGE_CODE_REGEX.match(normalized):
            raise ValueError(
                "Language must be a valid ISO 639-1 code (e.g., 'en', 'he')."
            )

        if normalized not in _SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language: {normalized}")

        object.__setattr__(self, "code", normalized)

    @property
    def name(self) -> str:
        return _SUPPORTED_LANGUAGES[self.code]

    def __str__(self) -> str:
        return self.code

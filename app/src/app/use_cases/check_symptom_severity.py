"""Check symptom severity. Mock: always returns medium (escalate)."""
from dataclasses import dataclass

from app.domain.types import SymptomSeverity


@dataclass
class CheckSymptomSeverityInput:
    user_id: str
    reported_text: str


@dataclass
class CheckSymptomSeverityResult:
    severity: SymptomSeverity
    reason: str | None = None


class CheckSymptomSeverity:
    """Mock: always medium so we always escalate; no medical advice."""

    def execute(self, input: CheckSymptomSeverityInput) -> CheckSymptomSeverityResult:
        return CheckSymptomSeverityResult(
            severity="medium",
            reason="Symptom reported; escalate to caregiver (mocked).",
        )

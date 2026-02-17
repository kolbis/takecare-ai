"""Check if marking dose as taken would be double-dose risk."""
from dataclasses import dataclass

from app.domain.types import DoubleDoseStatus
from app.repositories.dose_event_repository import DoseEventRepository


@dataclass
class CheckDoubleDoseRiskInput:
    user_id: str
    medication_id: str
    slot_time: str
    within_hours: float = 24.0


@dataclass
class CheckDoubleDoseRiskResult:
    status: DoubleDoseStatus
    reason: str | None = None


class CheckDoubleDoseRisk:
    def __init__(self, dose_event_repository: DoseEventRepository):
        self._repo = dose_event_repository

    def execute(self, input: CheckDoubleDoseRiskInput) -> CheckDoubleDoseRiskResult:
        recent = self._repo.get_recent_doses(
            user_id=input.user_id,
            medication_id=input.medication_id,
            slot_time=input.slot_time,
            within_hours=input.within_hours,
        )
        if recent:
            return CheckDoubleDoseRiskResult(
                status="RISK",
                reason=f"Already recorded {len(recent)} dose(s) for this slot in the last {input.within_hours}h",
            )
        return CheckDoubleDoseRiskResult(status="SAFE")

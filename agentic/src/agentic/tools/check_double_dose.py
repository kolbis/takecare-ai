from langchain_core.tools import tool
from agentic.tools.utils import get_container


@tool
def check_double_dose(
    user_id: str, medication_id: str, slot_time: str, within_hours: float = 24.0
) -> dict:
    """Check if marking this dose as taken would be double-dose risk. Returns status: SAFE or RISK, and optional reason."""
    c = get_container()
    from app.src.app.use_cases.check_double_dose_risk import CheckDoubleDoseRiskInput

    result = c.check_double_dose_risk.execute(
        CheckDoubleDoseRiskInput(
            user_id=user_id,
            medication_id=medication_id,
            slot_time=slot_time,
            within_hours=within_hours,
        )
    )
    return {"status": result.status, "reason": result.reason}

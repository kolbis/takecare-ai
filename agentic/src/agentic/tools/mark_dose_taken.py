from langchain_core.tools import tool
from agentic.tools.utils import get_container


@tool
def mark_dose_taken(
    user_id: str,
    medication_id: str,
    slot_time: str,
    dose_index: int = 0,
    source: str = "user_confirmed",
) -> dict:
    """Record that the user took the dose for the given medication/slot."""
    c = get_container()
    from app.src.app.use_cases.mark_dose_taken import MarkDoseTakenInput

    result = c.mark_dose_taken.execute(
        MarkDoseTakenInput(
            user_id=user_id,
            medication_id=medication_id,
            slot_time=slot_time,
            dose_index=dose_index,
            source=source,
        )
    )
    return {"success": result.success, "event_id": result.event_id}

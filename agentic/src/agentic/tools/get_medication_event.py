from langchain_core.tools import tool
from agentic.tools.utils import get_container


@tool
def get_medication_event(user_id: str, event_id: str | None = None) -> dict:
    """Get medication reminder event (current or by id). Returns medication_name, slot_time, reminder_id."""
    c = get_container()
    if event_id:
        result = c.get_medication_event.execute_by_id(event_id)
    else:
        result = c.get_medication_event.execute_current_for_user(user_id)
    if not result.event:
        return {"found": False}
    e = result.event
    return {
        "found": True,
        "reminder_id": e.id,
        "medication_id": e.medication_id,
        "medication_name": e.medication_name,
        "slot_time": e.slot_time,
        "dose_index": e.dose_index,
    }

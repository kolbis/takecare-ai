from langchain_core.tools import tool
from agentic.tools.utils import get_container


def _event_to_item(e):
    return {
        "reminder_id": e.id,
        "medication_id": e.medication_id,
        "medication_name": e.medication_name,
        "slot_time": e.slot_time,
        "dose_index": e.dose_index,
    }


@tool
def get_medication_event(user_id: str, event_id: str | None = None) -> dict:
    """Get current slot medication events (can be multiple per slot). Returns events list and, for backward compat, first event fields at top level."""
    c = get_container()
    if event_id:
        result = c.get_medication_event.execute_by_id(event_id)
    else:
        result = c.get_medication_event.execute_current_slot_for_user(user_id)
    if not result.events:
        return {"found": False, "events": []}
    events = result.events
    items = [_event_to_item(e) for e in events]
    first = items[0]
    return {
        "found": True,
        "reminder_id": first["reminder_id"],
        "medication_id": first["medication_id"],
        "medication_name": first["medication_name"],
        "slot_time": first["slot_time"],
        "dose_index": first["dose_index"],
        "events": items,
    }

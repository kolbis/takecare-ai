from langchain_core.tools import tool
from agentic.tools.utils import get_container


@tool
def snooze_dose(
    user_id: str,
    reminder_ids: list[str],
    snooze_minutes: int = 15,
) -> dict:
    """Snooze reminder(s). Pass one id to snooze one event, or all ids from current_reminder.medications to snooze the whole slot."""
    c = get_container()
    from app.src.app.use_cases.snooze_dose import SnoozeDoseInput

    if not reminder_ids:
        return {"success": False, "snooze_until": None}
    result = c.snooze_dose.execute(
        SnoozeDoseInput(
            user_id=user_id,
            reminder_ids=reminder_ids,
            snooze_minutes=snooze_minutes,
        )
    )
    return {
        "success": result.success,
        "snooze_until": str(result.snooze_until) if result.snooze_until else None,
    }

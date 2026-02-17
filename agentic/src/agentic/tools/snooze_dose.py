from langchain_core.tools import tool
from agentic.tools.utils import get_container


@tool
def snooze_dose(user_id: str, reminder_id: str, snooze_minutes: int = 15) -> dict:
    """Snooze the current reminder; next reminder at snooze_minutes from now."""
    c = get_container()
    from app.src.app.use_cases.snooze_dose import SnoozeDoseInput

    result = c.snooze_dose.execute(
        SnoozeDoseInput(
            user_id=user_id,
            reminder_id=reminder_id,
            snooze_minutes=snooze_minutes,
        )
    )
    return {
        "success": result.success,
        "snooze_until": str(result.snooze_until) if result.snooze_until else None,
    }

from langchain_core.tools import tool
from agentic.tools.utils import get_container


@tool
def notify_caregiver(
    user_id: str, reason: str, summary: str, severity: str | None = None
) -> dict:
    """Send escalation to caregiver (reason, summary). Mock: log only."""
    c = get_container()
    from app.src.app.use_cases.notify_caregiver import NotifyCaregiverInput

    result = c.notify_caregiver.execute(
        NotifyCaregiverInput(
            user_id=user_id,
            reason=reason,
            summary=summary,
            severity=severity,
        )
    )
    return {"success": result.success}

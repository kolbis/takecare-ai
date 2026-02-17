from langchain_core.tools import tool
from agentic.tools.utils import get_container


@tool
def get_user_profile(phone: str) -> dict:
    """Get user profile by phone number (language, caregiver_id, timezone)."""
    c = get_container()
    result = c.get_user_by_phone.execute(phone)
    if not result.user:
        return {"found": False, "user_id": None}
    u = result.user
    return {
        "found": True,
        "user_id": u.id,
        "phone": u.phone,
        "language": u.language,
        "caregiver_id": u.caregiver_id,
        "timezone": u.timezone,
        "name": u.name,
    }

from langchain_core.tools import tool
from agentic.tools.utils import get_container


@tool
def get_user_profile(phone: str) -> dict:
    """Get user profile by phone number (language, caregiver_ids, timezone, name)."""
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
        "caregiver_ids": u.caregiver_ids,
        "timezone": u.timezone,
        "first_name": u.first_name,
        "last_name": u.last_name,
        "age": u.age,
        "name": u.name,
    }

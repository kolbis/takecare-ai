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
    age = u.date_of_birth.age().value if u.date_of_birth else None
    name = f"{u.first_name} {u.last_name}".strip() or None
    return {
        "found": True,
        "user_id": str(u.id),
        "phone": str(u.phone),
        "language": u.language.code,
        "caregiver_ids": [str(c) for c in u.caregiver_ids],
        "timezone": str(u.timezone),
        "first_name": str(u.first_name),
        "last_name": str(u.last_name),
        "age": age,
        "name": name,
    }

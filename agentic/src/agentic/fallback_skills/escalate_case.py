"""Escalate case: notify_caregiver + set state for escalation copy."""
from typing import Any


def escalate_case(state: dict[str, Any], tools: Any, reason: str, summary: str) -> dict[str, Any]:
    user_id = state.get("user_id")

    tools["notify_caregiver"].invoke({
        "user_id": user_id,
        "reason": reason,
        "summary": summary,
    })

    return {
        "escalate_to_caregiver": True,
        "escalation_reason": reason,
    }

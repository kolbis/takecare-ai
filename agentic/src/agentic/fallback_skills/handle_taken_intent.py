"""Handle taken intent: check_double_dose → mark_dose_taken or escalate → send confirmation."""
from typing import Any

from shared.i18n import get_message, Language


def handle_taken_intent(state: dict[str, Any], tools: Any) -> dict[str, Any]:
    user_id = state.get("user_id")
    current_reminder = state.get("current_reminder") or {}
    language: Language = state.get("language") or "en"
    user_phone = state.get("user_phone") or ""

    medication_id = current_reminder.get("medication_id")
    slot_time = current_reminder.get("slot_time", "08:00")
    dose_index = current_reminder.get("dose_index", 0)

    # 1) Check double dose
    result = tools["check_double_dose"].invoke({
        "user_id": user_id,
        "medication_id": medication_id,
        "slot_time": slot_time,
    })
    status = result.get("status", "SAFE")

    reason = result.get("reason")
    if status == "SAFE":
        # 2a) Mark dose taken
        tools["mark_dose_taken"].invoke({
            "user_id": user_id,
            "medication_id": medication_id,
            "slot_time": slot_time,
            "dose_index": dose_index,
        })
        response_text = get_message("taken_confirmation", language)
        escalate = False
    else:
        # 2b) Escalate
        reason = reason or "Possible double dose"
        tools["notify_caregiver"].invoke({
            "user_id": user_id,
            "reason": "double_dose_risk",
            "summary": reason,
        })
        response_text = get_message("double_dose_message", language)
        escalate = True

    # 3) Send confirmation
    tools["send_whatsapp_message"].invoke({
        "to_phone": user_phone,
        "text": response_text,
    })

    return {
        "response_text": response_text,
        "escalate_to_caregiver": escalate,
        "escalation_reason": reason if status == "RISK" else None,
    }

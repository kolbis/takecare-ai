"""Handle snooze intent: snooze_dose → send confirmation."""
from typing import Any

from shared.i18n import get_message, Language


def handle_snooze_intent(state: dict[str, Any], tools: Any, snooze_minutes: int = 15) -> dict[str, Any]:
    user_id = state.get("user_id")
    current_reminder = state.get("current_reminder") or {}
    language: Language = state.get("language") or "en"
    user_phone = state.get("user_phone") or ""

    reminder_id = current_reminder.get("reminder_id", "rem1")

    # 1) Snooze
    tools["snooze_dose"].invoke({
        "user_id": user_id,
        "reminder_id": reminder_id,
        "snooze_minutes": snooze_minutes,
    })
    duration = f"{snooze_minutes} minutes"

    # 2) Send confirmation
    response_text = get_message("snooze_confirmation", language, duration=duration)
    tools["send_whatsapp_message"].invoke({
        "to_phone": user_phone,
        "text": response_text,
    })

    return {"response_text": response_text}

"""Generate reminder message: pull medication info, format EN/HE, attach buttons, send."""
from typing import Any

from shared.i18n import get_message, get_reminder_buttons, Language


def generate_reminder_message(state: dict[str, Any], tools: Any) -> dict[str, Any]:
    user_id = state.get("user_id")
    user_phone = state.get("user_phone") or ""
    language: Language = state.get("language") or "en"

    # 1) Pull medication info
    event_result = tools["get_medication_event"].invoke({"user_id": user_id})
    if not event_result.get("found"):
        response_text = get_message("reminder_body", language, medication_name="your medication")
    else:
        medication_name = event_result.get("medication_name", "your medication")
        response_text = get_message("reminder_body", language, medication_name=medication_name)

    # 2) Buttons in user language
    buttons = get_reminder_buttons(language)

    # 3) Send
    tools["send_whatsapp_message"].invoke({
        "to_phone": user_phone,
        "text": response_text,
        "buttons": buttons,
    })

    return {
        "response_text": response_text,
        "response_buttons": buttons,
    }

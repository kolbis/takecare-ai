"""Handle not sure intent: generate clarification question, send (no persistence)."""
from typing import Any

from shared.i18n import get_message, Language


def handle_not_sure_intent(state: dict[str, Any], tools: Any) -> dict[str, Any]:
    language: Language = state.get("language") or "en"
    user_phone = state.get("user_phone") or ""

    response_text = get_message("not_sure_clarify", language)
    tools["send_whatsapp_message"].invoke({
        "to_phone": user_phone,
        "text": response_text,
        "buttons": [
            {"id": "morning", "title": "This morning" if language == "en" else "הבוקר"},
            {"id": "earlier", "title": "Earlier" if language == "en" else "קודם"},
            {"id": "didnt_take", "title": "I didn't take it" if language == "en" else "לא נטלתי"},
        ],
    })

    return {"response_text": response_text}

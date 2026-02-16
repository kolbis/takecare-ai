"""Handle symptom report: check_symptom_severity → escalate → notify_caregiver → send safe message."""
from typing import Any

from shared.i18n import get_message, Language


def handle_symptom_report(state: dict[str, Any], tools: Any) -> dict[str, Any]:
    user_id = state.get("user_id")
    user_phone = state.get("user_phone") or ""
    language: Language = state.get("language") or "en"
    last_message = state.get("last_message_text") or ""

    # 1) Check severity
    result = tools["check_symptom_severity"].invoke({
        "user_id": user_id,
        "reported_text": last_message,
    })
    severity = result.get("severity", "medium")

    # 2) Escalate: notify caregiver
    tools["notify_caregiver"].invoke({
        "user_id": user_id,
        "reason": "symptom_reported",
        "summary": f"Symptom reported: {last_message[:200]}. Severity: {severity}.",
        "severity": severity,
    })

    # 3) Send safe message (no medical advice)
    response_text = get_message("escalation_disclaimer", language)
    tools["send_whatsapp_message"].invoke({
        "to_phone": user_phone,
        "text": response_text,
    })

    return {
        "response_text": response_text,
        "escalate_to_caregiver": True,
        "escalation_reason": "symptom_reported",
    }

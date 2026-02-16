from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from agentic.tools import (
    get_user_profile,
    get_medication_event,
    check_double_dose,
    mark_dose_taken,
    snooze_dose,
    notify_caregiver,
    send_whatsapp_message,
    check_symptom_severity,
)
from agentic.fallback_skills import (
    handle_taken_intent,
    handle_snooze_intent,
    handle_not_sure_intent,
    handle_symptom_report,
    escalate_case,
    generate_reminder_message,
)

if TYPE_CHECKING:
    from agentic.graph.state import TakeCareState

logger = logging.getLogger(__name__)

# Tools dict for legacy skills (fallback when deep agent not used)
TOOLS = {
    "get_user_profile": get_user_profile,
    "get_medication_event": get_medication_event,
    "check_double_dose": check_double_dose,
    "mark_dose_taken": mark_dose_taken,
    "snooze_dose": snooze_dose,
    "notify_caregiver": notify_caregiver,
    "send_whatsapp_message": send_whatsapp_message,
    "check_symptom_severity": check_symptom_severity,
}


def load_context(state: TakeCareState) -> dict[str, Any]:
    """Normalize input, load user profile, reminder context, set language. No LLM."""
    raw = state.get("raw_input") or {}
    # Assume raw has from (phone), message text, optional context (reminder id)
    from_phone = raw.get("from_phone") or raw.get("from") or "+1234567890"
    message_text = raw.get("message_text") or raw.get("text") or ""
    input_type = state.get("input_type") or "incoming_message"

    # Load user
    result = get_user_profile.invoke({"phone": from_phone})
    if not result.get("found"):
        return {
            "user_id": None,
            "user_phone": from_phone,
            "thread_id": from_phone,
            "language": "en",
            "last_message_text": message_text,
        }
    user_id = result["user_id"]
    language = result.get("language") or "en"

    # Load current reminder if reply-to-reminder or scheduled_reminder
    current_reminder = state.get("current_reminder")
    if not current_reminder and user_id:
        event_result = get_medication_event.invoke({"user_id": user_id})
        if event_result.get("found"):
            current_reminder = {
                "reminder_id": event_result["reminder_id"],
                "medication_id": event_result["medication_id"],
                "medication_name": event_result["medication_name"],
                "slot_time": event_result["slot_time"],
                "dose_index": event_result.get("dose_index", 0),
            }

    return {
        "user_id": user_id,
        "user_phone": from_phone,
        "thread_id": from_phone,
        "language": language,
        "current_reminder": current_reminder or {},
        "last_message_text": message_text,
    }


def deep_agent_node(state: TakeCareState) -> dict[str, Any]:
    """Invoke the DeepAgents orchestrator (Nurse, Safety Officer, Caregiver subagents + skills). Returns state updates."""
    from agentic.agents.deep_agent import invoke_agent
    thread_id = state.get("thread_id") or state.get("user_phone") or "default"
    try:
        return invoke_agent(dict(state), thread_id)
    except Exception as e:
        logger.exception("Deep agent invoke failed: %s", e)
        # Fallback: use legacy apply_action path with rule-based intent
        return _fallback_apply_action(state)


def _fallback_apply_action(state: TakeCareState) -> dict[str, Any]:
    """Fallback when deep agent fails: rule-based intent + legacy skills."""
    from shared.i18n import get_message
    last = (state.get("last_message_text") or "").strip().lower()
    raw = state.get("raw_input") or {}
    button_id = raw.get("button_id") or raw.get("interactive", {}).get("button_reply", {}).get("id")
    if button_id == "taken":
        proposed = "MARK_TAKEN"
        intent = "taken"
    elif button_id == "snooze":
        proposed = "SNOOZE"
        intent = "snooze"
    elif button_id == "not_sure":
        proposed = "CLARIFY"
        intent = "not_sure"
    elif "symptom" in last or "hurt" in last or "pain" in last:
        proposed = "ESCALATE"
        intent = "symptom"
    else:
        proposed = "CLARIFY"
        intent = "other"
    state_dict = dict(state)
    state_dict["proposed_action"] = proposed
    state_dict["intent"] = intent
    if proposed == "MARK_TAKEN":
        cur = state.get("current_reminder") or {}
        result = check_double_dose.invoke({
            "user_id": state["user_id"],
            "medication_id": cur.get("medication_id"),
            "slot_time": cur.get("slot_time", "08:00"),
        })
        if result.get("status") == "RISK":
            escalate_case(state_dict, TOOLS, reason=result.get("reason", "double_dose"), summary="")
            return {"response_text": get_message("double_dose_message", state.get("language") or "en"), "escalate_to_caregiver": True}
        return handle_taken_intent(state_dict, TOOLS)
    if proposed == "SNOOZE":
        return handle_snooze_intent(state_dict, TOOLS)
    if proposed == "CLARIFY" and intent == "not_sure":
        return handle_not_sure_intent(state_dict, TOOLS)
    if intent == "symptom":
        return handle_symptom_report(state_dict, TOOLS)
    return handle_not_sure_intent(state_dict, TOOLS)


def send_reminder(state: TakeCareState) -> dict[str, Any]:
    """For scheduled_reminder: generate and send reminder message (no user message)."""
    return generate_reminder_message(dict(state), TOOLS)


def finalize(state: TakeCareState) -> dict[str, Any]:
    """Ensure response_text/response_buttons are set for API to send. Notify caregiver if needed."""
    # Already sent by skills via send_whatsapp_message; just pass through
    return {
        "response_text": state.get("response_text") or "Done.",
        "response_buttons": state.get("response_buttons"),
    }

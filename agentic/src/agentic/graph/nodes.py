from __future__ import annotations

from typing import TYPE_CHECKING, Any

from agentic.tools import (
    get_user_profile,
    get_medication_event,
    send_whatsapp_message,
)

if TYPE_CHECKING:
    from agentic.graph.state import TakeCareState


def load_context(state: TakeCareState) -> dict[str, Any]:
    """Normalize input, load user profile, reminder context, set language. No LLM."""
    raw = state.get("raw_input") or {}
    # Assume raw has from (phone), message text, optional context (reminder id)
    from_phone = raw.get("from_phone") or raw.get("from") or "+1234567890"
    thread_id = raw.get("thread_id") or from_phone
    message_text = raw.get("message_text") or raw.get("text") or ""
    
    # TODO: remove this once we have a proper input type
    # input_type = state.get("input_type") or "incoming_message"

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

    # Load current reminder (can be multiple meds per slot). For scheduled_reminder always fetch slot events.
    current_reminder = state.get("current_reminder") if state.get("input_type") != "scheduled_reminder" else None
    if not current_reminder and user_id:
        event_result = get_medication_event.invoke({"user_id": user_id})
        if event_result.get("found") and event_result.get("events"):
            events_list = event_result["events"]
            slot_time = events_list[0].get("slot_time", "08:00") if events_list else "08:00"
            current_reminder = {
                "slot_time": slot_time,
                "medications": [
                    {
                        "medication_id": e["medication_id"],
                        "medication_name": e["medication_name"],
                        "dose_index": e.get("dose_index", 0),
                        "reminder_id": e["reminder_id"],
                    }
                    for e in events_list
                ],
            }

    return {
        "user_id": user_id,
        "user_phone": from_phone,
        "thread_id": thread_id,
        "language": language,
        "current_reminder": current_reminder or {},
        "last_message_text": message_text,
    }


def deep_agent_node(state: TakeCareState) -> dict[str, Any]:
    """Invoke the DeepAgents orchestrator (Nurse, Safety Officer, Caregiver subagents + skills). Returns state updates."""
    from agentic.agents.deep_agent import invoke_agent
    thread_id = state.get("thread_id") or state.get("user_phone") or "default"
    return invoke_agent(dict(state), thread_id)


def _format_medication_list(names: list[str]) -> str:
    """Format as 'A, B, and C'."""
    if not names:
        return ""
    if len(names) == 1:
        return names[0]
    return ", ".join(names[:-1]) + " and " + names[-1]


def send_reminder(state: TakeCareState) -> dict[str, Any]:
    """For scheduled_reminder: generate and send reminder message (no user message). Supports single or multiple medications."""
    from shared.i18n import get_message, get_reminder_buttons
    user_id = state.get("user_id")
    user_phone = state.get("user_phone") or ""
    language = state.get("language") or "en"
    event_result = get_medication_event.invoke({"user_id": user_id})
    if not event_result.get("found"):
        response_text = get_message("reminder_body", language, medication_name="your medication")
    else:
        events_list = event_result.get("events") or []
        names = [e.get("medication_name") or "your medication" for e in events_list]
        if len(names) <= 1:
            medication_name = names[0] if names else "your medication"
            response_text = get_message("reminder_body", language, medication_name=medication_name)
        else:
            medication_list = _format_medication_list(names)
            response_text = get_message(
                "reminder_body_multi", language, count=len(names), medication_list=medication_list
            )
    buttons = get_reminder_buttons(language)
    send_whatsapp_message.invoke({
        "to_phone": user_phone,
        "text": response_text,
        "buttons": buttons,
    })
    return {
        "response_text": response_text,
        "response_buttons": buttons,
    }


def finalize(state: TakeCareState) -> dict[str, Any]:
    """Ensure response_text/response_buttons are set for API to send. Notify caregiver if needed."""
    # TODO: need to design more structured output for the API to send.
    return {
        "response_text": state.get("response_text") or "Done.",
        "response_buttons": state.get("response_buttons"),
    }

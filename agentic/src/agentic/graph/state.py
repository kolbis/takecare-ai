from typing import Annotated, Literal

from langgraph.graph.message import add_messages, MessagesState


class TakeCareState(MessagesState, total=False):
    user_id: str
    user_phone: str
    thread_id: str
    input_type: Literal["incoming_message", "scheduled_reminder"]
    raw_input: dict
    language: Literal["en", "he"]
    messages: Annotated[list, add_messages]
    current_reminder: (
        dict  # slot_time: str, medications: list[{medication_id, medication_name, dose_index, reminder_id}]
    )
    intent: str  # taken, snooze, not_sure, no_medication, symptom, other
    safety_flags: dict
    escalate_to_caregiver: bool
    escalation_reason: str | None
    proposed_action: str  # MARK_TAKEN, SNOOZE, ESCALATE, CLARIFY
    response_text: str
    response_buttons: list
    events: list
    last_message_text: str

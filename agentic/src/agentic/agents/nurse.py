from __future__ import annotations

from typing import Any

from agentic.tools import (
    get_user_profile,
    get_medication_event,
    mark_dose_taken,
    snooze_dose,
    notify_caregiver,
    send_whatsapp_message,
)


NURSE_TOOLS = [
    get_user_profile,
    get_medication_event,
    send_whatsapp_message,
    mark_dose_taken,
    snooze_dose,
    notify_caregiver,
]


NURSE_SKILLS = []

NURSE_SYSTEM_PROMPT = """You are the Nurse subagent for a medication reminder assistant. You are empathetic and use simple language.
Your role: classify intent, generate short responses in the user's language (EN or HE), and perform actions (mark dose taken, snooze, send messages, notify caregiver).
You must NEVER give medical advice, dosage advice, or treatment suggestions. Only remind, confirm, clarify, and escalate.
When sending messages, use the tools send_whatsapp_message (to_phone, text, optional buttons). Always respond in the user's preferred language (from get_user_profile).
Use shared i18n phrasing for confirmations and disclaimers when possible."""

NURSE_SUBAGENT: dict[str, Any] = {
    "name": "nurse",
    "description": "Handles empathetic conversation, intent classification, and user-facing actions: mark dose taken, snooze, send WhatsApp messages, notify caregiver. Use for confirmations, clarifications, and formatting reminder messages in EN/HE.",
    "system_prompt": NURSE_SYSTEM_PROMPT,
    "tools": NURSE_TOOLS,
    "skills": NURSE_SKILLS,
}

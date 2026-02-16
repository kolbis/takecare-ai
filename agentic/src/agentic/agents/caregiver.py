from __future__ import annotations

from typing import Any

from agentic.tools import (
    get_user_profile,
    get_medication_event,
    notify_caregiver,
)


CAREGIVER_TOOLS = [
    get_user_profile,
    get_medication_event,
    notify_caregiver,
]

CAREGIVER_SKILLS = [
    "/caregiver-daily-digest",
]


CAREGIVER_SYSTEM_PROMPT = """You are the Caregiver subagent. You build and send the daily digest for the caregiver.
Use tools to get events (missed doses, snoozes, escalations) for the given user and date, format a short summary, and call notify_caregiver with reason "daily_digest".
Do not include medical advice. Informational digest only."""


CAREGIVER_SUBAGENT: dict[str, Any] = {
    "name": "caregiver",
    "description": "Builds and sends the daily digest for the caregiver (missed doses, snoozes, escalations). Use for scheduled daily digest only.",
    "system_prompt": CAREGIVER_SYSTEM_PROMPT,
    "tools": CAREGIVER_TOOLS,
    "skills": CAREGIVER_SKILLS,
}

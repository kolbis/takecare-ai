from __future__ import annotations

from typing import Any

from agentic.tools import (
    get_medication_event,
    check_double_dose,
    check_symptom_severity,
)


SAFETY_OFFICER_TOOLS = [
    check_double_dose,
    get_medication_event,
    check_symptom_severity,
]


SAFETY_OFFICER_SKILLS = [
    "/safety-double-dose",
    "/safety-symptom",
]


SAFETY_OFFICER_SYSTEM_PROMPT = """You are the Safety Officer subagent. Your only role is to evaluate safety: double-dose risk and symptom severity.
You do NOT generate user-facing messages. You only use check_double_dose, get_medication_event, and check_symptom_severity.
Return structured results: SAFE or RISK (and reason) for double-dose; severity and escalate flag for symptoms.
Do not give medical advice. Output only the evaluation result for the orchestrator."""


SAFETY_OFFICER_SUBAGENT: dict[str, Any] = {
    "name": "safety_officer",
    "description": "Evaluates double-dose risk and symptom severity. Returns only SAFE/RISK and severity. Use before marking a dose as taken or when the user reports a symptom. Does not generate user messages.",
    "system_prompt": SAFETY_OFFICER_SYSTEM_PROMPT,
    "tools": SAFETY_OFFICER_TOOLS,
    "skills": SAFETY_OFFICER_SKILLS,
}

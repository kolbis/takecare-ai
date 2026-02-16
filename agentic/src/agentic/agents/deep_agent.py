from __future__ import annotations

import os
from typing import Any

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from langgraph.checkpoint.memory import MemorySaver
from agentic.agents import NURSE_SUBAGENT, SAFETY_OFFICER_SUBAGENT, CAREGIVER_SUBAGENT

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

# Path to skills (TakeCare: agentic/skills/) for FilesystemBackend
# From .../agentic/src/agentic/agents/deep_agent.py -> .../agentic
_AGENTIC_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)
SKILLS_ROOT = os.path.join(_AGENTIC_ROOT, "skills")

# All tools for main agent and subagents that need them
ORCHESTRATOR_TOOLS = [
    get_user_profile,
    get_medication_event,
    check_double_dose,
    mark_dose_taken,
    snooze_dose,
    notify_caregiver,
    send_whatsapp_message,
    check_symptom_severity,
]


# Main agent routing skills (paths relative to backend root)
ORCHESTRATOR_SKILLS = [
    "/medication-reminder-taken",
    "/medication-reminder-snooze",
    "/medication-reminder-not-sure",
    "/medication-reminder-symptom",
    "/generate-reminder-message",
]

ORCHESTRATOR_SYSTEM_PROMPT = """You are the coordinator for a medication reminder assistant. The user is an elderly person on WhatsApp.
You have subagents: Nurse (conversation and actions), Safety Officer (double-dose and symptom checks), Caregiver (daily digest).
Use your skills to decide which flow to run. For "taken" confirmations, always delegate to Safety Officer first to check double-dose risk, then to Nurse.
For scheduled reminders (no user message), use the generate-reminder-message skill and delegate to Nurse.
Respond in the user's language (EN or HE). Never give medical advice. Escalate to caregiver when needed."""


_backend: FilesystemBackend | None = None
_agent: Any = None
_checkpointer = MemorySaver()


def get_model() -> str:
    return os.getenv("ORCHESTRATOR_MODEL", "openai:gpt-4o-mini")


def _get_backend() -> FilesystemBackend:
    global _backend
    if _backend is None:
        _backend = FilesystemBackend(root_dir=SKILLS_ROOT)
    return _backend


def get_agent():
    """Build and return the compiled orchestrator agent (cached)."""
    global _agent
    if _agent is not None:
        return _agent
    backend = _get_backend()
    model = get_model()
    subagents = [NURSE_SUBAGENT, SAFETY_OFFICER_SUBAGENT, CAREGIVER_SUBAGENT]
    _agent = create_deep_agent(
        model=model,
        tools=ORCHESTRATOR_TOOLS,
        system_prompt=ORCHESTRATOR_SYSTEM_PROMPT,
        skills=ORCHESTRATOR_SKILLS,
        subagents=subagents,
        backend=backend,
        checkpointer=_checkpointer,
    )
    return _agent


def invoke_agent(state: dict[str, Any], thread_id: str) -> dict[str, Any]:
    """
    Invoke the deep agent with state from the graph; return state updates (response_text, response_buttons, escalate_to_caregiver, escalation_reason).
    """
    from langchain_core.messages import HumanMessage

    user_message = _state_to_user_message(state)
    agent = get_agent()
    config = {"configurable": {"thread_id": thread_id}}
    result = agent.invoke(
        {"messages": [HumanMessage(content=user_message)]},
        config=config,
    )
    return _result_to_state_updates(result, state)

# TODO: this is not the place for this. Need to think about how to handle this.

def _state_to_user_message(state: dict[str, Any]) -> str:
    """Build a single user message that encodes the current turn for the deep agent."""
    parts = [
        "User message: " + (state.get("last_message_text") or "(none)"),
        "User language: " + (state.get("language") or "en"),
        "Input type: " + (state.get("input_type") or "incoming_message"),
        "User ID: " + (state.get("user_id") or ""),
        "User phone: " + (state.get("user_phone") or ""),
    ]
    current_reminder = state.get("current_reminder") or {}
    if current_reminder:
        parts.append("Current reminder: " + str(current_reminder))
    return "\n".join(parts)


def _result_to_state_updates(
    result: dict[str, Any], state: dict[str, Any]
) -> dict[str, Any]:
    """Extract response_text, response_buttons, escalate_to_caregiver, escalation_reason from agent result."""
    messages = result.get("messages") or []
    response_text = ""
    escalate_to_caregiver = False
    escalation_reason = None
    for m in reversed(messages):
        if hasattr(m, "content") and m.content and isinstance(m.content, str):
            response_text = m.content
            break
    # Heuristic: if response mentions caregiver or escalation, set flags
    if "caregiver" in response_text.lower() or "notified" in response_text.lower():
        escalate_to_caregiver = True
        escalation_reason = "escalation"
    return {
        "response_text": response_text or state.get("response_text") or "Done.",
        "response_buttons": state.get("response_buttons"),
        "escalate_to_caregiver": escalate_to_caregiver,
        "escalation_reason": escalation_reason,
    }

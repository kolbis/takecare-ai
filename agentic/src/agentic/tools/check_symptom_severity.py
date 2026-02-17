from langchain_core.tools import tool
from agentic.tools.utils import get_container


@tool
def check_symptom_severity(user_id: str, reported_text: str) -> dict:
    """Classify reported symptom severity for escalation. Returns severity (low/medium/high/emergency). Mock: always medium."""
    c = get_container()
    from app.src.app.use_cases.check_symptom_severity import CheckSymptomSeverityInput

    result = c.check_symptom_severity.execute(
        CheckSymptomSeverityInput(user_id=user_id, reported_text=reported_text)
    )
    return {"severity": result.severity, "reason": result.reason}

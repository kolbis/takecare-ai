"""LangChain tools that delegate to app use cases."""
from langchain_core.tools import tool

# Lazy container to avoid circular import at module load
def _container():
    from app.container import get_container
    return get_container()


@tool
def get_user_profile(phone: str) -> dict:
    """Get user profile by phone number (language, caregiver_id, timezone)."""
    c = _container()
    result = c.get_user_by_phone.execute(phone)
    if not result.user:
        return {"found": False, "user_id": None}
    u = result.user
    return {
        "found": True,
        "user_id": u.id,
        "phone": u.phone,
        "language": u.language,
        "caregiver_id": u.caregiver_id,
        "timezone": u.timezone,
        "name": u.name,
    }


@tool
def get_medication_event(user_id: str, event_id: str | None = None) -> dict:
    """Get medication reminder event (current or by id). Returns medication_name, slot_time, reminder_id."""
    c = _container()
    if event_id:
        result = c.get_medication_event.execute_by_id(event_id)
    else:
        result = c.get_medication_event.execute_current_for_user(user_id)
    if not result.event:
        return {"found": False}
    e = result.event
    return {
        "found": True,
        "reminder_id": e.id,
        "medication_id": e.medication_id,
        "medication_name": e.medication_name,
        "slot_time": e.slot_time,
        "dose_index": e.dose_index,
    }


@tool
def check_double_dose(user_id: str, medication_id: str, slot_time: str, within_hours: float = 24.0) -> dict:
    """Check if marking this dose as taken would be double-dose risk. Returns status: SAFE or RISK, and optional reason."""
    c = _container()
    from app.use_cases.check_double_dose_risk import CheckDoubleDoseRiskInput
    result = c.check_double_dose_risk.execute(
        CheckDoubleDoseRiskInput(
            user_id=user_id,
            medication_id=medication_id,
            slot_time=slot_time,
            within_hours=within_hours,
        )
    )
    return {"status": result.status, "reason": result.reason}


@tool
def mark_dose_taken(user_id: str, medication_id: str, slot_time: str, dose_index: int = 0, source: str = "user_confirmed") -> dict:
    """Record that the user took the dose for the given medication/slot."""
    c = _container()
    from app.use_cases.mark_dose_taken import MarkDoseTakenInput
    result = c.mark_dose_taken.execute(
        MarkDoseTakenInput(
            user_id=user_id,
            medication_id=medication_id,
            slot_time=slot_time,
            dose_index=dose_index,
            source=source,
        )
    )
    return {"success": result.success, "event_id": result.event_id}


@tool
def snooze_dose(user_id: str, reminder_id: str, snooze_minutes: int = 15) -> dict:
    """Snooze the current reminder; next reminder at snooze_minutes from now."""
    c = _container()
    from app.use_cases.snooze_dose import SnoozeDoseInput
    result = c.snooze_dose.execute(
        SnoozeDoseInput(
            user_id=user_id,
            reminder_id=reminder_id,
            snooze_minutes=snooze_minutes,
        )
    )
    return {"success": result.success, "snooze_until": str(result.snooze_until) if result.snooze_until else None}


@tool
def notify_caregiver(user_id: str, reason: str, summary: str, severity: str | None = None) -> dict:
    """Send escalation to caregiver (reason, summary). Mock: log only."""
    c = _container()
    from app.use_cases.notify_caregiver import NotifyCaregiverInput
    result = c.notify_caregiver.execute(
        NotifyCaregiverInput(
            user_id=user_id,
            reason=reason,
            summary=summary,
            severity=severity,
        )
    )
    return {"success": result.success}


@tool
def send_whatsapp_message(to_phone: str, text: str, buttons: list[dict] | None = None) -> dict:
    """Send a WhatsApp message to the user (text and optional quick reply buttons). Mock: log only."""
    import logging
    logging.getLogger(__name__).info(
        "send_whatsapp_message (mocked): to=%s text=%s buttons=%s",
        to_phone, text[:80], buttons,
    )
    return {"sent": True, "mocked": True}


@tool
def check_symptom_severity(user_id: str, reported_text: str) -> dict:
    """Classify reported symptom severity for escalation. Returns severity (low/medium/high/emergency). Mock: always medium."""
    c = _container()
    from app.use_cases.check_symptom_severity import CheckSymptomSeverityInput
    result = c.check_symptom_severity.execute(
        CheckSymptomSeverityInput(user_id=user_id, reported_text=reported_text)
    )
    return {"severity": result.severity, "reason": result.reason}

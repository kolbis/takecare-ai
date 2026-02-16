"""Scheduler: fire reminders at due time, retries on no response, missed -> escalate. Mock: in-memory due list."""
import logging
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


class ReminderScheduler:
    """Mock: no real cron. Provides trigger_reminder(user_id, reminder_context) for API/cron to call."""

    def trigger_reminder(self, user_id: str, user_phone: str, reminder_id: str | None = None) -> dict[str, Any]:
        """Invoke graph with input_type=scheduled_reminder to send reminder message."""
        try:
            from agentic.graph import graph
            result = graph.invoke(
                {
                    "raw_input": {
                        "from_phone": user_phone,
                        "message_text": "",
                        "scheduled_reminder": True,
                        "reminder_id": reminder_id,
                    },
                    "input_type": "scheduled_reminder",
                    "current_reminder": {"reminder_id": reminder_id or "rem1"},
                },
                config={"configurable": {"thread_id": user_phone or user_id}},
            )
            return {"ok": True, "response_text": result.get("response_text")}
        except Exception as e:
            logger.exception("trigger_reminder failed: %s", e)
            return {"ok": False, "error": str(e)}

    def trigger_retry(self, user_id: str, user_phone: str, reminder_id: str) -> dict[str, Any]:
        """Retry reminder (same as trigger_reminder for now)."""
        return self.trigger_reminder(user_id, user_phone, reminder_id)

    def mark_missed_and_escalate(self, user_id: str, user_phone: str, reminder_id: str) -> dict[str, Any]:
        """After N retries: mark missed, notify caregiver. Mock: call app NotifyCaregiver."""
        try:
            from app.container import get_container
            from app.use_cases.notify_caregiver import NotifyCaregiverInput
            c = get_container()
            c.notify_caregiver.execute(
                NotifyCaregiverInput(
                    user_id=user_id,
                    reason="missed_dose",
                    summary=f"User did not respond to reminder {reminder_id} after retries.",
                )
            )
            return {"ok": True}
        except Exception as e:
            logger.exception("mark_missed_and_escalate failed: %s", e)
            return {"ok": False, "error": str(e)}


_scheduler: ReminderScheduler | None = None


def get_reminder_scheduler() -> ReminderScheduler:
    global _scheduler
    if _scheduler is None:
        _scheduler = ReminderScheduler()
    return _scheduler

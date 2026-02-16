"""Routes for scheduler (cron triggers)."""
from fastapi import APIRouter
from pydantic import BaseModel

from api.scheduler import get_reminder_scheduler

router = APIRouter(prefix="/scheduler", tags=["scheduler"])


class TriggerReminderRequest(BaseModel):
    user_id: str
    user_phone: str
    reminder_id: str | None = None


@router.post("/trigger-reminder")
def trigger_reminder(body: TriggerReminderRequest):
    """Called by cron: trigger reminder for user (sends WhatsApp via graph)."""
    s = get_reminder_scheduler()
    return s.trigger_reminder(body.user_id, body.user_phone, body.reminder_id)


@router.post("/mark-missed")
def mark_missed(body: TriggerReminderRequest):
    """After N retries: mark missed and notify caregiver."""
    s = get_reminder_scheduler()
    return s.mark_missed_and_escalate(body.user_id, body.user_phone, body.reminder_id or "rem1")

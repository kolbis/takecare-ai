from agentic.tools.get_user_profile import get_user_profile
from agentic.tools.get_medication_event import get_medication_event
from agentic.tools.check_double_dose import check_double_dose
from agentic.tools.mark_dose_taken import mark_dose_taken
from agentic.tools.snooze_dose import snooze_dose
from agentic.tools.notify_caregiver import notify_caregiver
from agentic.tools.send_whatsapp_message import send_whatsapp_message
from agentic.tools.check_symptom_severity import check_symptom_severity


ALL_TOOLS = [
    get_user_profile,
    get_medication_event,
    check_double_dose,
    mark_dose_taken,
    snooze_dose,
    notify_caregiver,
    send_whatsapp_message,
    check_symptom_severity,
]

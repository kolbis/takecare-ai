"""EN + HE messages for reminders, confirmations, escalation."""
from typing import Literal, List, Dict, Any

Language = Literal["en", "he"]

# Keys used by agentic/skills and api
MESSAGE_KEYS = [
    "reminder_body",
    "reminder_buttons_taken",
    "reminder_buttons_snooze",
    "reminder_buttons_not_sure",
    "taken_confirmation",
    "snooze_confirmation",
    "not_sure_clarify",
    "escalation_disclaimer",
    "double_dose_message",
]

_MESSAGES: Dict[str, Dict[str, str]] = {
    "reminder_body": {
        "en": "Time for your {medication_name}. Did you take it?",
        "he": "זמן ל-{medication_name}. נטלת?",
    },
    "reminder_buttons_taken": {
        "en": "Taken ✅",
        "he": "נטלתי ✅",
    },
    "reminder_buttons_snooze": {
        "en": "Remind later ⏰",
        "he": "תזכיר אחר כך ⏰",
    },
    "reminder_buttons_not_sure": {
        "en": "Not sure 🤔",
        "he": "לא בטוח 🤔",
    },
    "taken_confirmation": {
        "en": "Got it, marked as taken. Stay well.",
        "he": "מעולה, סימנתי שנטלת. להתראות.",
    },
    "snooze_confirmation": {
        "en": "I'll remind you again in {duration}.",
        "he": "אזכיר שוב בעוד {duration}.",
    },
    "not_sure_clarify": {
        "en": "When do you think you might have taken it – this morning or earlier? Reply with the time or 'I didn't take it'.",
        "he": "מתי נראה לך שנטלת – הבוקר או קודם? ענה עם השעה או 'לא נטלתי'.",
    },
    "escalation_disclaimer": {
        "en": "This isn't medical advice. We've notified your caregiver. If you feel unwell, contact a doctor or caregiver.",
        "he": "זה לא ייעוץ רפואי. עדכנו את המטפל. אם אתה לא מרגיש טוב, פנה לרופא או למטפל.",
    },
    "double_dose_message": {
        "en": "To stay safe, we've notified your caregiver. Do not take another dose until they confirm.",
        "he": "לבטיחותך עדכנו את המטפל. אל תיקח מנה נוספת עד שיאשרו.",
    },
}


def get_message(key: str, lang: Language, **format_kwargs: Any) -> str:
    msg = _MESSAGES.get(key, {}).get(lang, _MESSAGES.get(key, {}).get("en", key))
    if format_kwargs:
        return msg.format(**format_kwargs)
    return msg


def get_reminder_buttons(lang: Language) -> List[Dict[str, str]]:
    return [
        {"id": "taken", "title": get_message("reminder_buttons_taken", lang)},
        {"id": "snooze", "title": get_message("reminder_buttons_snooze", lang)},
        {"id": "not_sure", "title": get_message("reminder_buttons_not_sure", lang)},
    ]

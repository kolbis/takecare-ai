"""Send WhatsApp messages (template, text, interactive buttons). Mock: log only."""
import logging
from typing import Any

logger = logging.getLogger(__name__)


class WhatsAppSender:
    """Mock: log only. Replace with Meta Cloud API / provider client for production."""

    def __init__(self, phone_number_id: str | None = None, access_token: str | None = None):
        self.phone_number_id = phone_number_id
        self.access_token = access_token

    def send_text(self, to_phone: str, text: str) -> dict[str, Any]:
        logger.info("WhatsAppSender.send_text (mocked): to=%s text=%s", to_phone, text[:80])
        return {"sent": True, "mocked": True}

    def send_template(self, to_phone: str, template_name: str, language: str, components: list[Any] | None = None) -> dict[str, Any]:
        logger.info(
            "WhatsAppSender.send_template (mocked): to=%s template=%s lang=%s",
            to_phone, template_name, language,
        )
        return {"sent": True, "mocked": True}

    def send_interactive_buttons(self, to_phone: str, body: str, buttons: list[dict[str, str]]) -> dict[str, Any]:
        logger.info(
            "WhatsAppSender.send_interactive_buttons (mocked): to=%s body=%s buttons=%s",
            to_phone, body[:80], buttons,
        )
        return {"sent": True, "mocked": True}


def get_whatsapp_sender() -> WhatsAppSender:
    return WhatsAppSender()

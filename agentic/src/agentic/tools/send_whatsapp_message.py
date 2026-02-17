from langchain_core.tools import tool

# TODO: Implement this

@tool
def send_whatsapp_message(
    to_phone: str, text: str, buttons: list[dict] | None = None
) -> dict:
    """Send a WhatsApp message to the user (text and optional quick reply buttons). Mock: log only."""
    import logging

    logging.getLogger(__name__).info(
        "send_whatsapp_message (mocked): to=%s text=%s buttons=%s",
        to_phone,
        text[:80],
        buttons,
    )
    return {"sent": True, "mocked": True}

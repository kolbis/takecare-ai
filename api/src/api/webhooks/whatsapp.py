"""WhatsApp webhook: verify (GET), ingest (POST), invoke graph."""
import logging
from typing import Any

from fastapi import APIRouter, Request, Query, Response

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhooks/whatsapp", tags=["webhooks"])

# In production, load from env
VERIFY_TOKEN = "med-verify-token"


@router.get("", response_model=None)
def verify_webhook(
    request: Request,
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
):
    """Meta webhook verification: return hub.challenge if token matches."""
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return Response(content=hub_challenge or "")
    return Response(status_code=403)


@router.post("")
async def handle_webhook(request: Request) -> dict[str, str]:
    """Parse Meta payload, normalize, invoke graph, return 200 quickly. Processing can be async."""
    body = await request.json()
    # Normalize to internal format
    raw = _normalize_webhook_payload(body)
    if not raw:
        return {"status": "ok"}

    # Invoke graph (sync for now; can enqueue job for async)
    try:
        from agentic.graph import graph
        result = graph.invoke(
            {
                "raw_input": raw,
                "input_type": "incoming_message",
            },
            config={"configurable": {"thread_id": raw.get("from_phone", "unknown")}},
        )
        logger.info("Graph result: response_text=%s", (result.get("response_text") or "")[:80])
    except Exception as e:
        logger.exception("Graph invoke failed: %s", e)

    return {"status": "ok"}


def _normalize_webhook_payload(body: dict[str, Any]) -> dict[str, Any] | None:
    """Extract from Meta webhook format to internal: from_phone, message_text, button_id."""
    try:
        entry = (body.get("entry") or [{}])[0]
        changes = (entry.get("changes") or [{}])[0]
        value = changes.get("value") or {}
        messages = value.get("messages") or []
        if not messages:
            return None
        msg = messages[0]
        from_phone = msg.get("from")
        if not from_phone:
            return None
        # Normalize phone to E.164-like
        from_phone = str(from_phone) if not str(from_phone).startswith("+") else f"+{from_phone}"

        message_text = ""
        button_id = None
        msg_type = msg.get("type", "")
        if msg_type == "text":
            message_text = (msg.get("text") or {}).get("body") or ""
        elif msg_type == "button":
            button = msg.get("button") or {}
            message_text = button.get("text") or ""
            button_id = button.get("payload") or button.get("id")
        elif msg_type == "interactive":
            interactive = msg.get("interactive") or {}
            br = interactive.get("button_reply") or {}
            button_id = br.get("id")
            message_text = br.get("title") or ""

        return {
            "from_phone": from_phone,
            "message_text": message_text,
            "button_id": button_id,
            "message_id": msg.get("id"),
            "raw": msg,
        }
    except (IndexError, KeyError, TypeError):
        return None

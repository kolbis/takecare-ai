"""FastAPI app: webhooks, WhatsApp, caregiver notifications."""
from contextlib import asynccontextmanager
from fastapi import FastAPI

from api.webhooks.whatsapp import router as whatsapp_router
from api.routes.scheduler import router as scheduler_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="Med API", lifespan=lifespan)

app.include_router(whatsapp_router)
app.include_router(scheduler_router)


@app.get("/health")
def health():
    return {"status": "ok"}

from fastapi import APIRouter

from app.api.routes.chat import router as chat_router
from app.api.routes.triage import router as triage_router
from app.api.routes.attention import router as attention_router

api_router = APIRouter()

api_router.include_router(chat_router, prefix="/chat", tags=["Chat"])
api_router.include_router(triage_router, prefix="/triage", tags=["Triage"])
api_router.include_router(attention_router, prefix="/attention", tags=["Attention"])
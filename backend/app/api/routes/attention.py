from app.models.attention import (
    AttentionRequest,
    AttentionResponse,
)
from app.services.attention_service import AttentionService
from fastapi import APIRouter

router = APIRouter()

service = AttentionService()


@router.post("", response_model=AttentionResponse)
def attention(request: AttentionRequest):
    return service.generate(request)

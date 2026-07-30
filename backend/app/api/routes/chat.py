from app.models.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from fastapi import APIRouter

router = APIRouter()

service = ChatService()


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest):

    return service.chat(request)

from app.assistant.graph import assistant
from app.core.logger import logger
from app.models.chat import ChatRequest, ChatResponse


class ChatService:
    def chat(self, request: ChatRequest):
        logger.info(
            "Session %s - Nuevo mensaje: %s", request.session_id, request.message
        )
        try:
            result = assistant.chat(
                session_id=request.session_id, message=request.message
            )
            last_message = result["messages"][-1]
            return ChatResponse(
                reply=last_message.content,
                conversation_finished=result["interview_completed"],
            )
        except Exception as e:
            logger.error(
                "Session %s - Error al procesar el mensaje: %s",
                request.session_id,
                str(e),
            )
            raise

from app.assistant.graph import assistant
from app.core.logger import current_session_id, logger, session_log_handler
from app.models.chat import ChatRequest, ChatResponse
from langchain_core.messages import HumanMessage


class ChatService:
    def chat(self, request: ChatRequest):
        token = current_session_id.set(request.session_id)
        logger.info(
            "Session %s - Nuevo mensaje de usuario: %s", request.session_id, request.message
        )
        try:
            result = assistant.chat(
                session_id=request.session_id, message=request.message
            )
            messages = result.get("messages", [])
            last_message = messages[-1] if messages else None
            reply_content = last_message.content if last_message else ""

            # Extraer llamadas a RAG y sus resultados ÚNICAMENTE del turno actual
            rag_logs = []
            tool_calls_map = {}

            last_human_idx = -1
            for i in range(len(messages) - 1, -1, -1):
                msg = messages[i]
                if isinstance(msg, HumanMessage) or getattr(msg, "type", None) == "human":
                    last_human_idx = i
                    break

            current_turn_messages = messages[last_human_idx:] if last_human_idx != -1 else messages

            for msg in current_turn_messages:
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    for tc in msg.tool_calls:
                        if tc.get("name") == "retrieve_medical_protocol":
                            tool_calls_map[tc.get("id")] = tc.get("args", {}).get("query", "")
                elif getattr(msg, "type", None) == "tool" or msg.__class__.__name__ == "ToolMessage":
                    tool_id = getattr(msg, "tool_call_id", None)
                    query = tool_calls_map.get(tool_id, "Consulta de protocolo")
                    rag_logs.append({
                        "query": query,
                        "retrieved_content": str(msg.content)
                    })

            system_logs = session_log_handler.get_logs(request.session_id)

            return ChatResponse(
                reply=reply_content,
                conversation_finished=result.get("interview_completed", False),
                rag_logs=rag_logs,
                system_logs=system_logs,
            )
        except Exception as e:
            logger.error(
                "Session %s - Error al procesar el mensaje: %s",
                request.session_id,
                str(e),
            )
            raise
        finally:
            current_session_id.reset(token)



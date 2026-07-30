from app.assistant.graph import assistant
from app.core.logger import current_session_id, logger, session_log_handler
from app.models.attention import (
    AttentionRequest,
    AttentionResponse,
)


class AttentionService:
    def generate(self, request: AttentionRequest):
        token = current_session_id.set(request.session_id)
        logger.info("Session %s - Iniciando generación de atención médica estructurada", request.session_id)
        try:
            triage = assistant.triage(request.session_id)

            attention = assistant.attention(
                session_id=request.session_id,
                triage_result=triage,
            )

            system_logs = session_log_handler.get_logs(request.session_id)

            return AttentionResponse(
                triage=triage["triage"],
                prioridad=triage["prioridad"],
                especialidad_sugerida=attention["especialidad_sugerida"],
                resumen_clinico=attention["resumen_clinico"],
                system_logs=system_logs,
            )
        except Exception as e:
            logger.error(
                "Session %s - Error al generar atención: %s",
                request.session_id,
                str(e),
            )
            raise
        finally:
            current_session_id.reset(token)


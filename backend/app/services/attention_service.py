from app.assistant.graph import assistant
from app.core.logger import logger
from app.models.attention import (
    AttentionRequest,
    AttentionResponse,
)


class AttentionService:
    def generate(self, request: AttentionRequest):
        logger.info("Session %s - Generando atención", request.session_id)
        try:
            triage = assistant.triage(request.session_id)

            attention = assistant.attention(
                session_id=request.session_id,
                triage_result=triage,
            )

            return AttentionResponse(
                triage=triage["triage"],
                prioridad=triage["prioridad"],
                especialidad_sugerida=attention["especialidad_sugerida"],
                resumen_clinico=attention["resumen_clinico"],
            )
        except Exception as e:
            logger.error(
                "Session %s - Error al generar atención: %s",
                request.session_id,
                str(e),
            )
            raise

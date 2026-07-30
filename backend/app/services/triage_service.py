from app.assistant.graph import assistant
from app.core.logger import logger
from app.models.triage import TriageRequest, TriageResponse


class TriageService:
    def classify(self, request: TriageRequest):
        logger.info("Session %s - Clasificando triage", request.session_id)
        try:
            result = assistant.triage(request.session_id)
            return TriageResponse(
                triage=result["triage"],
                prioridad=result["prioridad"],
                justificacion=result["triage_justification"],
            )
        except Exception as e:
            logger.error(
                "Session %s - Error al clasificar triage: %s",
                request.session_id,
                str(e),
            )
            raise

from pydantic import BaseModel


class AttentionRequest(BaseModel):
    session_id: str


class AttentionResponse(BaseModel):
    triage: str
    prioridad: str
    especialidad_sugerida: str
    resumen_clinico: str

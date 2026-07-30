from pydantic import BaseModel, Field


class AttentionRequest(BaseModel):
    session_id: str


class AttentionResponse(BaseModel):
    triage: str
    prioridad: str
    especialidad_sugerida: str
    resumen_clinico: str
    system_logs: list[str] = Field(default_factory=list)


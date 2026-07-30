from pydantic import BaseModel


class TriageRequest(BaseModel):
    session_id: str


class TriageResponse(BaseModel):
    triage: str
    prioridad: str
    justificacion: str

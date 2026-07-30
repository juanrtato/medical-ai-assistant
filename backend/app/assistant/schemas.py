from typing import Literal

from pydantic import BaseModel


class InterviewOutput(BaseModel):
    reply: str
    interview_completed: bool


class TriageOutput(BaseModel):
    triage: Literal["I", "II", "III", "IV"]
    prioridad: Literal["Emergencia inmediata", "Urgente", "Prioritario", "No urgente"]
    justificacion: str


class AttentionOutput(BaseModel):
    triage: str
    prioridad: str
    especialidad_sugerida: str
    resumen_clinico: str

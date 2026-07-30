from typing import Annotated

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class ClinicalState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    protocol_context: str
    question_count: int
    interview_completed: bool

    triage: str | None
    prioridad: str | None
    triage_justification: str | None

    especialidad_sugerida: str | None
    resumen_clinico: str | None

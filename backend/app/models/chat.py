from typing import Literal

from pydantic import BaseModel, Field, field_validator


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    session_id: str = Field(..., description="Identificador de la conversación")
    message: str = Field(..., min_length=1)

    @field_validator("message")
    @classmethod
    def validate_message(cls, value):

        if not value.strip():
            raise ValueError("Message cannot be empty")

        return value


class ChatResponse(BaseModel):
    reply: str
    conversation_finished: bool
    rag_logs: list[dict] = Field(default_factory=list, description="Logs de las consultas RAG realizadas")
    system_logs: list[str] = Field(default_factory=list, description="Logs completos de la ejecución del sistema")



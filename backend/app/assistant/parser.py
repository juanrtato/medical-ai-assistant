from app.llm.client import llm
from pydantic import BaseModel


class InterviewOutput(BaseModel):
    reply: str
    interview_completed: bool


structured_parser = llm.with_structured_output(
    InterviewOutput
)  # Parser for structured interview responses


def parse_response(text: str):
    """
    Parse the response from the assistant to determine if the interview has been completed.
    """
    prompt = f"""
    Analiza la siguiente respuesta del auxiliar de enfermería digital.

    Indica si la respuesta es una conclusión/cierre final de la entrevista o si continúa preguntando al paciente.

    Devuelve:
    - reply: el texto analizado
    - interview_completed: true ÚNICAMENTE si el mensaje despide/cierra la entrevista e indica que la información fue registrada (y NO incluye nuevas preguntas con '?').
    - interview_completed: false si el mensaje contiene cualquier pregunta o solicitud de información nueva.

    Respuesta:

    {text}
    """

    return structured_parser.invoke(prompt)

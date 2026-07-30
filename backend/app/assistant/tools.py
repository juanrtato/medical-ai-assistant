from app.core.logger import logger
from app.rag.retriever import retrieve_protocol
from langchain.tools import tool


@tool
def retrieve_medical_protocol(query: str) -> str:
    """Busca y recupera el protocolo médico oficial o guía clínica relevante.
    
    CUÁNDO USAR:
    - Únicamente cuando el paciente mencione un síntoma clínico principal o síndrome relevante (ej. 'fiebre', 'dolor de pecho', 'cefalea', 'dificultad respiratoria') para conocer las preguntas recomendadas y signos de alarma de dicho protocolo.
    
    CUÁNDO NO USAR:
    - No la uses para saludos ('Hola', 'Buenos días').
    - No la uses para respuestas cortas del usuario sobre duración o intensidad (ej. 'Desde ayer', 'Es un 7 de 10').
    - No la uses si ya recuperaste el protocolo para el mismo síntoma en la conversación.
    
    REGLA PARA EL QUERY:
    - El parámetro 'query' debe ser una lista corta de términos clínicos clave en español (ej: 'protocolo fiebre signos de alarma' o 'dolor toracico triage'), NO pegues el mensaje completo del paciente.
    """
    logger.info("[Tool Call] Invocando 'retrieve_medical_protocol' con query='%s'", query)
    result = retrieve_protocol(query)
    logger.info("[Tool Call] 'retrieve_medical_protocol' finalizado con %d caracteres.", len(result))
    return result



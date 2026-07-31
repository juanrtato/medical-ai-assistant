from app.assistant.agent import agent
from app.assistant.parser import parse_response
from app.assistant.prompts import ATTENTION_PROMPT, SYSTEM_PROMPT, TRIAGE_PROMPT
from app.assistant.schemas import AttentionOutput, TriageOutput
from app.assistant.state import ClinicalState
from app.core.logger import logger
from app.llm.client import llm
from langchain_core.messages import HumanMessage, SystemMessage

MAX_QUESTIONS = 10


def agent_node(state: ClinicalState):
    """
    Node that invokes the agent to process user messages and determine the next action.
    """
    messages = state.get("messages", [])
    logger.info(
        "[Node: Agent] Invocando agente con %d mensajes en historial", len(messages)
    )

    human_msg_count = sum(
        1
        for m in messages
        if isinstance(m, HumanMessage) or getattr(m, "type", None) == "human"
    )

    current_system_prompt = SYSTEM_PROMPT
    if human_msg_count >= MAX_QUESTIONS:
        current_system_prompt += f"\n\n--- INSTRUCCIÓN DE CIERRE OBLIGATORIO ---\nHas alcanzado el límite máximo de {MAX_QUESTIONS} mensajes del usuario. NO HAGAS NINGUNA PREGUNTA MÁS. Agradece amablemente al paciente por la información suministrada y confirma que la recolección de síntomas ha finalizado para proceder a la clasificación de triage."

    non_system_messages = [
        m
        for m in messages
        if not isinstance(m, SystemMessage) and getattr(m, "type", None) != "system"
    ]
    messages_with_system = [
        SystemMessage(content=current_system_prompt)
    ] + non_system_messages

    response = agent.invoke(messages_with_system)

    interview_completed = state.get("interview_completed", False)

    if hasattr(response, "tool_calls") and response.tool_calls:
        logger.info(
            "[Node: Agent] El modelo determinó llamar a herramienta(s): %s",
            [tc.get("name") for tc in response.tool_calls],
        )
    else:
        logger.info("[Node: Agent] El modelo generó respuesta directa sin herramientas")
        if human_msg_count >= MAX_QUESTIONS:
            interview_completed = True
            logger.info(
                "[Node: Agent] Se alcanzó el número máximo de preguntas de entrevista (%d). Marcar entrevista finalizada.",
                MAX_QUESTIONS,
            )
        elif response.content:
            try:
                parsed = parse_response(response.content)
                if parsed.interview_completed:
                    interview_completed = True
                    logger.info(
                        "[Node: Agent] El parser detectó que la entrevista ha finalizado."
                    )
            except Exception as e:
                logger.warning(
                    "[Node: Agent] No se pudo analizar fin de entrevista: %s", str(e)
                )

    return {
        "messages": [response],
        "interview_completed": interview_completed,
    }


interview_node = agent_node


def triage_node(state):
    """
    Node that invokes the triage process based on the current state of the conversation.
    """

    logger.info(
        "[Node: Triage] Invocando análisis de triage con %d mensajes en historial",
        len(state.get("messages", [])),
    )
    structured_llm = llm.with_structured_output(TriageOutput)

    tool_messages = [
        m
        for m in state.get("messages", [])
        if getattr(m, "type", None) == "tool" or m.__class__.__name__ == "ToolMessage"
    ]
    rag_context = (
        "\n\n".join([str(m.content) for m in tool_messages])
        if tool_messages
        else "Sin protocolo RAG adicional."
    )

    messages = [
        SystemMessage(
            content=f"{TRIAGE_PROMPT}\n\n--- PROTOCOLOS CLÍNICOS RAG RELEVANTES ---\n{rag_context}"
        ),
        *state["messages"],
    ]
    response = structured_llm.invoke(messages)
    logger.info(
        "[Node: Triage] Resultado obtenido -> Triage: %s | Prioridad: %s",
        response.triage,
        response.prioridad,
    )
    return {
        "triage": response.triage,
        "prioridad": response.prioridad,
        "triage_justification": response.justificacion,
    }


def attention_node(state, triage):
    """
    Node that invokes the attention process based on the current state of the conversation and the triage result.
    """
    logger.info(
        "[Node: Attention] Invocando generación de resumen y atención médica para Triage %s",
        triage.get("triage"),
    )
    structured_llm = llm.with_structured_output(AttentionOutput)

    tool_messages = [
        m
        for m in state.get("messages", [])
        if getattr(m, "type", None) == "tool" or m.__class__.__name__ == "ToolMessage"
    ]
    rag_context = (
        "\n\n".join([str(m.content) for m in tool_messages])
        if tool_messages
        else "Sin protocolo RAG adicional."
    )

    messages = [
        SystemMessage(
            content=f"""
            {ATTENTION_PROMPT}

            --- CLASIFICACIÓN DE TRIAGE REALIZADA ---
            Triage: {triage["triage"]}
            Prioridad: {triage["prioridad"]}
            Justificación: {triage.get("triage_justification", "")}

            --- PROTOCOLOS CLÍNICOS RAG UTILIZADOS ---
            {rag_context}
            """
        ),
        *state["messages"],
    ]

    response = structured_llm.invoke(messages)
    logger.info(
        "[Node: Attention] Resumen clínico y sugerencia generados. Especialidad: %s",
        response.especialidad_sugerida,
    )

    return {
        "especialidad_sugerida": response.especialidad_sugerida,
        "resumen_clinico": response.resumen_clinico,
    }

from app.assistant.prompts import ATTENTION_PROMPT, SYSTEM_PROMPT, TRIAGE_PROMPT
from app.assistant.schemas import AttentionOutput, InterviewOutput, TriageOutput
from app.assistant.state import ClinicalState
from app.llm.client import llm
from langchain_core.messages import AIMessage, SystemMessage

MAX_QUESTIONS = 5


def interview_node(state: ClinicalState):

    question_count = state.get("question_count", 0)

    if question_count >= MAX_QUESTIONS:
        return {"interview_completed": True}

    messages = [SystemMessage(content=SYSTEM_PROMPT), *state["messages"]]

    structured_llm = llm.with_structured_output(InterviewOutput)

    response = structured_llm.invoke(messages)

    return {
        "messages": [AIMessage(content=response.reply)],
        "interview_completed": response.interview_completed,
        "question_count": question_count + 1,
    }


def triage_node(state):
    structured_llm = llm.with_structured_output(TriageOutput)
    messages = [SystemMessage(content=TRIAGE_PROMPT), *state["messages"]]
    response = structured_llm.invoke(messages)
    return {
        "triage": response.triage,
        "prioridad": response.prioridad,
        "triage_justification": response.justificacion,
    }


def attention_node(state, triage):

    structured_llm = llm.with_structured_output(AttentionOutput)

    messages = [
        SystemMessage(
            content=f"""
            {ATTENTION_PROMPT}

            La clasificación de triage ya fue realizada.

            Triage: {triage["triage"]}
            Prioridad: {triage["prioridad"]}
            Justificación: {triage["triage_justification"]}
            """
        ),
        *state["messages"],
    ]

    response = structured_llm.invoke(messages)

    return {
        "especialidad_sugerida": response.especialidad_sugerida,
        "resumen_clinico": response.resumen_clinico,
    }

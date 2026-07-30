import uuid

import streamlit as st
from services.api import attention, chat

st.set_page_config(
    page_title="Emermédica AI",
    page_icon="🚑",
    layout="wide",
)


st.title("🚑 Emermédica AI")
st.subheader("Asistente Inteligente de Atención Médica")


st.markdown("""
Asistente basado en Inteligencia Artificial para apoyar la captura
de síntomas, clasificación de triage y generación de atención médica
estructurada.

⚠️ Este sistema funciona como auxiliar de enfermería digital.
No realiza diagnósticos médicos.
""")


with st.sidebar:
    st.header("Configuración")

    st.info("Estado del servicio: Activo")

    if st.button("Nueva conversación"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.session_state.conversation_finished = False
        st.session_state.attention = None

        st.rerun()

    st.divider()
    st.header("📊 Logs del RAG")
    all_rag_logs = []
    for msg in st.session_state.get("messages", []):
        if msg.get("rag_logs"):
            all_rag_logs.extend(msg["rag_logs"])

    if all_rag_logs:
        st.caption(f"Total de consultas RAG ejecutadas: {len(all_rag_logs)}")
        for idx, log in enumerate(all_rag_logs, 1):
            with st.expander(f"📌 RAG #{idx}: {log['query']}"):
                st.code(log["retrieved_content"], language="text")
    else:
        st.caption("Aún no se han realizado búsquedas RAG.")

    st.divider()
    st.header("📟 Consola del Sistema (Full Logs)")
    all_system_logs = []
    assistant_msgs = [m for m in st.session_state.get("messages", []) if m.get("system_logs")]
    if assistant_msgs:
        all_system_logs = list(assistant_msgs[-1]["system_logs"])

    if st.session_state.get("attention_logs"):
        all_system_logs.extend(st.session_state["attention_logs"])

    if all_system_logs:
        logs_text = "\n".join(all_system_logs)
        st.code(logs_text, language="log")
    else:
        st.caption("Sin eventos registrados en consola.")


# Inicializar sesión

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())


if "messages" not in st.session_state:
    st.session_state.messages = []


if "conversation_finished" not in st.session_state:
    st.session_state.conversation_finished = False


if "attention" not in st.session_state:
    st.session_state.attention = None


# Mostrar conversación

for msg_idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat

if (
    prompt := st.chat_input("Describe tus síntomas...")
) and not st.session_state.conversation_finished:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.spinner("Analizando información clínica..."):
            response = chat(
                st.session_state.session_id,
                prompt,
            )

        assistant_response = response["reply"]

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": assistant_response,
                "rag_logs": response.get("rag_logs", []),
                "system_logs": response.get("system_logs", []),
            }
        )

        st.session_state.conversation_finished = response["conversation_finished"]

        st.rerun()

    except Exception as e:
        st.error("No fue posible comunicarse con el servicio.")

        st.exception(e)


# Generar atención

if st.session_state.conversation_finished:
    st.success("Entrevista finalizada correctamente.")

    if st.button("Generar atención") and st.session_state.attention is None:
        try:
            with st.spinner("Generando atención médica estructurada..."):
                att_res = attention(st.session_state.session_id)
                st.session_state.attention = att_res
                st.session_state["attention_logs"] = att_res.get("system_logs", [])

            st.rerun()

        except Exception as e:
            st.error("Error generando la atención médica.")

            st.exception(e)


# Mostrar resultado

if st.session_state.attention:
    result = st.session_state.attention

    st.divider()

    st.subheader("📋 Atención médica generada")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Nivel de triage",
            result["triage"],
        )

    with col2:
        st.write(f"**Prioridad:** {result['prioridad']}")

    st.write(f"**Especialidad sugerida:** {result['especialidad_sugerida']}")

    st.write("### Resumen clínico")

    st.write(result["resumen_clinico"])

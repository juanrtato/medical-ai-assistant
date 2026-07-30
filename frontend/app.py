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

for message in st.session_state.messages:
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
                st.session_state.attention = attention(st.session_state.session_id)

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

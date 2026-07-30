from app.assistant.nodes import interview_node
from langchain_core.messages import HumanMessage

state = {
    "messages": [HumanMessage(content="Tengo fiebre desde ayer")],
    "interview_completed": False,
    "triage": None,
    "prioridad": None,
    "specialty": None,
    "summary": None,
}

result = interview_node(state)

print(result)

from app.assistant.graph import clinical_graph
from langchain_core.messages import HumanMessage

state = {
    "messages": [HumanMessage(content="Tengo fiebre desde ayer")],
    "interview_completed": False,
    "triage": None,
    "prioridad": None,
    "specialty": None,
    "summary": None,
}

result = clinical_graph.invoke(state, config={"configurable": {"thread_id": "test_thread"}})

print(result)

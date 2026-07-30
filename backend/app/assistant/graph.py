from app.assistant.nodes import (
    attention_node,
    interview_node,
    triage_node,
)
from app.assistant.state import ClinicalState
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph


class ClinicalAssistant:
    def __init__(self):

        builder = StateGraph(ClinicalState)

        builder.add_node("interview", interview_node)

        builder.add_edge(START, "interview")
        builder.add_edge("interview", END)

        memory = MemorySaver()

        self.graph = builder.compile(checkpointer=memory)

    def chat(self, session_id: str, message: str):

        state = {
            "messages": [HumanMessage(content=message)],
            "interview_completed": False,
        }

        return self.graph.invoke(
            state, config={"configurable": {"thread_id": session_id}}
        )

    def _get_state(self, session_id: str):

        snapshot = self.graph.get_state(
            config={"configurable": {"thread_id": session_id}}
        )

        return snapshot.values

    def triage(self, session_id: str):

        state = self._get_state(session_id)

        return triage_node(state)

    def attention(self, session_id: str, triage_result: dict):

        state = self._get_state(session_id)

        return attention_node(state, triage_result)


assistant = ClinicalAssistant()

from app.assistant.nodes import (
    agent_node,
    attention_node,
    triage_node,
)
from app.assistant.state import ClinicalState
from app.assistant.tools import retrieve_medical_protocol
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

tool_node = ToolNode([retrieve_medical_protocol])


class ClinicalAssistant:
    def __init__(self):

        builder = StateGraph(ClinicalState)

        builder.add_node("agent", agent_node)
        builder.add_node("tools", tool_node)

        builder.add_edge(START, "agent")
        builder.add_conditional_edges("agent", tools_condition)
        builder.add_edge("tools", "agent")

        memory = MemorySaver()

        self.graph = builder.compile(checkpointer=memory)

    def chat(self, session_id: str, message: str):
        """
        Process a chat message from the user.
        """

        state = {
            "messages": [HumanMessage(content=message)],
            "interview_completed": False,
        }

        return self.graph.invoke(
            state, config={"configurable": {"thread_id": session_id}}
        )

    def _get_state(self, session_id: str):
        """
        Get the current state of a session.
        """

        snapshot = self.graph.get_state(
            config={"configurable": {"thread_id": session_id}}
        )

        return snapshot.values

    def triage(self, session_id: str):
        """
        Perform triage on the current state of a session.
        """

        state = self._get_state(session_id)

        return triage_node(state)

    def attention(self, session_id: str, triage_result: dict):
        """
        Perform attention on the current state of a session.
        """

        state = self._get_state(session_id)

        return attention_node(state, triage_result)


assistant = ClinicalAssistant()
clinical_graph = assistant.graph

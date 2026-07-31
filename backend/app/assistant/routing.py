from langgraph.graph import END


def should_continue(state):
    last = state["messages"][-1]
    """
    Determine if the conversation should continue based on the last message.
    """

    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tools"

    return END

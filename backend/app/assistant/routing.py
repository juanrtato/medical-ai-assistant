from langgraph.graph import END


def should_continue(state):
    last = state["messages"][-1]

    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tools"

    return END


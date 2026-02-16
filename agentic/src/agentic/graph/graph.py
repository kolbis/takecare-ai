from typing import Literal

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from agentic.graph.state import TakeCareState
from agentic.graph.nodes import (
    load_context,
    deep_agent_node,
    finalize,
    send_reminder,
)


def _after_load_context(state: TakeCareState) -> Literal["send_reminder", "deep_agent"]:
    """Route: scheduled_reminder -> send_reminder; else -> deep_agent_node."""
    if state.get("input_type") == "scheduled_reminder":
        return "send_reminder"
    return "deep_agent"


def build_graph():
    workflow = StateGraph(TakeCareState)

    workflow.add_node("load_context", load_context)
    workflow.add_node("send_reminder", send_reminder)
    workflow.add_node("deep_agent", deep_agent_node)
    workflow.add_node("finalize", finalize)

    workflow.add_edge(START, "load_context")
    workflow.add_conditional_edges(
        "load_context",
        _after_load_context,
        {"send_reminder": "send_reminder", "deep_agent": "deep_agent"},
    )
    workflow.add_edge("send_reminder", "finalize")
    workflow.add_edge("deep_agent", "finalize")
    workflow.add_edge("finalize", END)

    return workflow


# Compiled graph with in-memory checkpointer for thread persistence
memory = MemorySaver()
graph = build_graph().compile(checkpointer=memory)

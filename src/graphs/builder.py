from langgraph.graph import StateGraph, START, END

from graphs.nodes import get_request_type, fetch_fields_names, fill_request_fields, create_ticket
from graphs.nodes.routing_functions import can_fetch_fields, can_create_ticket
from graphs.state import OverallState
from graphs.context import ContextSchema

def build_graph():
    graph = StateGraph(state_schema=OverallState, context_schema=ContextSchema)
    graph.add_node("get_request_type", get_request_type)
    graph.add_node("fetch_fields_names", fetch_fields_names)
    graph.add_node("fill_request_fields", fill_request_fields)
    graph.add_node("create_ticket", create_ticket)

    graph.add_edge(START, "get_request_type")
    graph.add_conditional_edges(
        "get_request_type", 
        can_fetch_fields,
        ["fetch_fields_names", END]
    )
    graph.add_edge("fetch_fields_names", "fill_request_fields")
    graph.add_conditional_edges(
        "fill_request_fields",
        can_create_ticket,
        ["create_ticket", END]
    )
    graph.add_edge("create_ticket", END)

    return graph.compile()

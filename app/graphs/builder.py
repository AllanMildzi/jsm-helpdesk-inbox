from langgraph.graph import StateGraph, START, END

from graphs.nodes import get_request_type, fetch_fields_names, fill_request_fields, create_ticket
from graphs.state import OverallState

def build_graph():
    graph = StateGraph(state_schema=OverallState)
    graph.add_node("get_request_type", get_request_type.get_request_type)
    graph.add_node("fetch_fields_names", fetch_fields_names.fetch_fields_names)
    graph.add_node("fill_request_fields", fill_request_fields.fill_request_fields)
    graph.add_node("create_ticket", create_ticket.create_ticket)

    graph.add_edge(START, "get_request_type")
    graph.add_edge("get_request_type", "fetch_fields_names")
    graph.add_edge("fetch_fields_names", "fill_request_fields")
    graph.add_edge("fill_request_fields", "create_ticket")
    graph.add_edge("create_ticket", END)

    return graph.compile()

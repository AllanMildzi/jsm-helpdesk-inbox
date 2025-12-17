from langgraph.graph import END
from pyparsing import Literal

from graphs.state import OverallState

def can_create_ticket(state: OverallState) -> Literal["create_ticket", END]:
    if state.request_field_values:
        return "create_ticket"
    
    return END
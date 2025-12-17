from langgraph.graph import END
from pyparsing import Literal

from graphs.state import OverallState

def can_fetch_fields(state: OverallState) -> Literal["fetch_fields_names", END]:
    if state.request_type_id and state.request_type_id != -1:
        return "fetch_fields_names"
    
    return END
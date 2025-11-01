from graphs.state import OverallState
from core import Config
from models.request_body import RequestBody
from jsm import ServiceDesk

def create_ticket(state: OverallState) -> OverallState:
    type_id = state.request_type_id
    field_values = state.request_field_values

    request_body = RequestBody(requestFieldValues=field_values,
                               requestTypeId=type_id,
                               serviceDeskId=Config.SERVICE_DESK_ID)
    
    ServiceDesk.create_request(request_body)

    return state
from graphs.state import OverallState
from core import Config
from models import RequestBody, RequestOutput
from jsm import ServiceDesk

def create_ticket(state: OverallState) -> OverallState:
    type_id = state.request_type_id
    field_values = state.request_field_values

    request_body = RequestBody(requestFieldValues=field_values,
                               requestTypeId=type_id,
                               serviceDeskId=Config.SERVICE_DESK_ID)
    
    output = ServiceDesk.create_request(request_body)

    # Finds the value of the summary from the 'requestFieldValues' list of the output payload
    # since the list contains other fields (description, attachement, etc...)
    summary_value = next(
        (
            field.get("value") for field in output.get("requestFieldValues") 
            if field.get("fieldId") == "summary"
        ),
        None
    )

    request_output = RequestOutput(issueKey=output.get("issueKey"),
                                   summary=summary_value,
                                   link=output.get("_links").get("web"))

    return {"request_output": request_output}
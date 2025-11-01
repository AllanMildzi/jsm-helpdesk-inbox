import json

from graphs.state import OverallState
from chains.extract_request_fields import extract_request_fields
from utils import extract_json_from_string

def fill_request_fields(state: OverallState) -> OverallState:
    email = state.email
    fields = state.request_field_names

    fields_json = [field.model_dump_json(indent=2) for field in fields]

    request_fields_json = extract_json_from_string(extract_request_fields(email.get_text(), fields_json))

    field_values = json.loads(request_fields_json)

    print(f"Filled request fields: {field_values}")

    return {"request_field_values": field_values}
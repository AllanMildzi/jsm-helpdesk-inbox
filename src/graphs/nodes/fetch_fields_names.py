from graphs.state import OverallState
from jsm import ServiceDesk
from utils import get_logger

logger = get_logger(__name__)

def fetch_fields_names(state: OverallState) -> OverallState:
    request_type = state.request_type_id

    field_names = ServiceDesk.get_request_fields_names(request_type)

    logger.debug(f"Fetched field names: {field_names}")

    return {"request_field_names": field_names}
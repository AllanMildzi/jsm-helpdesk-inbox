from graphs.state import OverallState
from chains.extract_request_type import extract_request_type
from jsm import ServiceDesk
from utils import get_logger

logger = get_logger(__name__)

def get_request_type(state: OverallState) -> OverallState:
    email = state.email

    request_type = extract_request_type(email.get_content(), ServiceDesk.REQUEST_TYPES_LIST)

    logger.debug(f"Extracted request type ID: {request_type}")

    return {"request_type_id": request_type}
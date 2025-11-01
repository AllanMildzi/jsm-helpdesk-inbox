from pydantic import BaseModel, Field
from typing import Any, List, Dict, Optional

from models.message import Message
from models.request_field import RequestField

class OverallState(BaseModel):
    email: Optional[Message] = Field(
        default=None,
        description="Email message")
    
    request_type_id: Optional[int] = Field(
        default=None,
        description="Extracted request type from the email")
    
    request_field_names: Optional[List[RequestField]] = Field(
        default=None,
        description="Fetched request fields name")
    
    request_field_values: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Extracted request fields values from the email")
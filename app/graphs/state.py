from pydantic import BaseModel, Field, ConfigDict
from typing import Any, List, Dict, Optional
from email.message import EmailMessage

from models import RequestField, RequestOutput

class OverallState(BaseModel):
    email: Optional[EmailMessage] = Field(
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
    
    request_output: Optional[RequestOutput] = Field(
        default=None,
        description="Output object received after request is created")
    
    # Allow to work with arbitrary classes such as EmailMessage from the email library
    model_config = ConfigDict(arbitrary_types_allowed=True)

class OutputState(BaseModel):
    email: Optional[EmailMessage] = Field(
        default=None,
        description="Email message")
    
    # Same as above
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
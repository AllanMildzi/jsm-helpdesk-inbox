from pydantic import BaseModel, Field
from typing import Optional, Any, Dict

class RequestBody(BaseModel):
    requestFieldValues: Dict[str, Any] = Field(description="Fields of the request"),
    requestTypeId: int = Field(description="ID of the request type"),
    serviceDeskId: int = Field(description="ID of the Service Desk"),
    isAdfRequest: Optional[bool] = Field(default=False, 
                                         description="Whether to accept rich text fields in Atlassian Document Format")
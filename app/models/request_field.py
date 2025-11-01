from pydantic import BaseModel, Field
from typing import Optional, List

from models.valid_value import ValidValue

class RequestField(BaseModel):
    fieldId: str = Field(description="ID of the field")
    name: str = Field(description="Name of the field")
    validValues: Optional[List[ValidValue]] = Field(
        default=[],
        description="Description of the request")
from pydantic import BaseModel, Field

class ValidValue(BaseModel):
    label: str = Field(description="Label of the valid value")
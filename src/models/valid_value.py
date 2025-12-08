from pydantic import BaseModel, Field

class ValidValue(BaseModel):
    value: str = Field(description="Value of the valid value")
    label: str = Field(description="Label of the valid value")
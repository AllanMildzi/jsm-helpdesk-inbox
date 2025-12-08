from pydantic import BaseModel, Field

class RequestType(BaseModel):
    id: str = Field(description="ID of the request type")
    name : str = Field(description="Name of the request type")
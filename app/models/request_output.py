from pydantic import BaseModel, Field

class RequestOutput(BaseModel):
    issueKey: str = Field(default=None, description="Key of the request")
    summary: str = Field(default=None, description="Summary of the request")
    link: str = Field(default=None, description="Link to the portal")
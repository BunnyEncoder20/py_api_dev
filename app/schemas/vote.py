from pydantic import BaseModel, Field

# Pydantic Model for Validation
class Votes_PyModel(BaseModel):
    post_id: int
    dir: int = Field(..., le=1, ge=0)
from pydantic import BaseModel, Field
from typing import List, Optional, Union
from datetime import datetime


# Pydantic Model for Validation
class Post_Model(BaseModel):
    # _id: int
    title: str
    content: str
    published: bool
    tags: List = []

# Pydantic Model for Standardized responses
class Response_Model(BaseModel):
    status_code: int
    msg: Optional[str] = Field(default=None, description="Optional message string")
    data: Optional[dict] = Field(default=None, description="Optional data payload")

    class Config:
        orm_mode: True

# Pydantic Model for Standardized Reponses V2 (we directly send the object we receive from DB as res)
# * We can omit the fields , we do not want to send to the frontend / client
class Response_Model_V2(BaseModel):
    # id: int
    title: str
    content: str
    published: bool
    tags: List
    # created_at: datetime
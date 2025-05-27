from pydantic import BaseModel, Field
from typing import List, Optional, Union


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
    data: Optional[Union[dict, Post_Model]] = Field(default=None, description="Optional data payload")
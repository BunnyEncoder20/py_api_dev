from pydantic import BaseModel
from typing import List

# Pydantic Model for Validation
class Post_PyModel(BaseModel):
    # _id: int
    title: str
    content: str
    published: bool
    tags: List = []

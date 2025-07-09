from pydantic import BaseModel
from typing import List

# These are data validation schemas hence are under the schemas folder

# Pydantic Model for Validation
class Post_PyModel(BaseModel):
    # _id: int
    title: str
    content: str
    published: bool
    tags: List = []

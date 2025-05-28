from pydantic import BaseModel, Field
from typing import List, Optional, Union
from datetime import datetime

# Pydantic Model for Validation
class Post_PyModel(BaseModel):
    # _id: int
    title: str
    content: str
    published: bool
    tags: List = []
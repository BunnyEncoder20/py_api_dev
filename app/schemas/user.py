from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Union
from datetime import datetime

# Pydantic Model for Validation
class UserCreate_PyModel(BaseModel):
    email: EmailStr
    password: str
    
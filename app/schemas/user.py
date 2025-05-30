from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Union
from datetime import datetime

# Pydantic Model for Validation
class register_user_PyModel(BaseModel):
    email: EmailStr
    password: str

class login_user_PyModel(BaseModel):
    email: EmailStr
    password: str

class user_token_PyModel(BaseModel):
    id: int
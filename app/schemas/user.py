from datetime import datetime
from pydantic import BaseModel, EmailStr

# Pydantic Model for Validation
class User_PyModel(BaseModel):
    id: int
    email: EmailStr
    password: str
    created_at: datetime

class Register_user_PyModel(BaseModel):
    email: EmailStr
    password: str

class Login_user_PyModel(BaseModel):
    email: EmailStr
    password: str

class User_token_PyModel(BaseModel):
    id: int

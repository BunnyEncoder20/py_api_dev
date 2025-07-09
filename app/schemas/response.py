from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import List, Optional
from datetime import datetime

# Pydantic Model for Standardized responses
class Response_PyModel(BaseModel):
    status_code: int
    msg: Optional[str] = Field(default=None, description="Optional message string")
    data: Optional[dict] = Field(default=None, description="Optional data payload")

    # For Pydantic v1
    # class Config:
    #     orm_mode=True

    # For Pydantic v2 onwards
    model_config = ConfigDict(from_attributes=True)


# Pydantic Model for returning user data
class User_Response_PyModel(BaseModel):
    id: int
    email: EmailStr
    # password: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)



# Pydantic Model for returning only specified fields
# We can omit the fields , we do not want to send to the frontend / client
class Response_PyModel_V2(BaseModel):
    # id: int
    title: str
    content: str
    published: bool
    tags: List
    created_at: datetime
    # user_id: int
    user: User_Response_PyModel     # this is the name of the Pydantic model of User resp

    model_config = ConfigDict(from_attributes=True)


class Votes_PyModel(BaseModel):
    posts: Response_PyModel_V2
    votes: int

    model_config = ConfigDict(from_attributes=True)


class Token_Reponse_PyModel(BaseModel):
    status: int
    msg: str
    token_type: str
    access_token: str

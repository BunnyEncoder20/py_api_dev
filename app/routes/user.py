from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from random import randint
from typing import List

from app.schemas.response import Response_PyModel_V2
from app.schemas.user import User_PyModel

router = APIRouter(
    prefix="/posts",
    tags=["Users"]
)
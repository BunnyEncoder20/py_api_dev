from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from random import randint
from typing import List

from app.schemas.response import Response_Model, Response_Model_V2
from app.schemas.post import Post_Model

router = APIRouter(
    prefix="/posts",
    tags=["Users"]
)
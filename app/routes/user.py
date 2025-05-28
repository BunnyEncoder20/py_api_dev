from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from random import randint
from typing import List

from app.schemas.response import Response_PyModel_V2
from app.schemas.user import User_PyModel
from app.models.user import Users

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/", response_model=List[Response_PyModel_V2])
def get_users(db: Session = Depends(get_db)):
    '''get all users'''
    data = db.query(Users).all()
    
    # sending res
    return data
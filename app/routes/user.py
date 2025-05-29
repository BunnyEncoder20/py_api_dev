from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from random import randint
from typing import List

from app.schemas.response import User_Response_PyModel
from app.schemas.user import register_user_PyModel
from app.models.user import Users
from app.database import get_db

router = APIRouter(
    prefix="/v1/api/users",
    tags=["Users"]
)

@router.get("/")
def get_users(db: Session = Depends(get_db)):
    '''get all users'''
    data = db.query(Users).all()
    
    # sending res
    return data

@router.post("/register", response_model=User_Response_PyModel)
def register_user(puser: register_user_PyModel, db: Session = Depends(get_db)):
    new_user = Users(**puser.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

    

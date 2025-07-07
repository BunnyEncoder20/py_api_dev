from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.schemas.response import User_Response_PyModel
from app.schemas.user import register_user_PyModel
from app.models.user import Users
from app.database import get_db
from app.utils.encryption import hash_pwd

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

@router.get("/{pid}", response_model=User_Response_PyModel)
def get_specifi_user(pid: int, db: Session = Depends(get_db)):
    '''get users by ID'''
    user = db.query(Users).filter(Users.id == pid).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id[{pid}] does not exist"
        )
    
    # sending res
    return user

@router.post("/register", response_model=User_Response_PyModel)
def register_user(puser: register_user_PyModel, db: Session = Depends(get_db)):
    puser.password = hash_pwd(puser.password)
    new_user = Users(**puser.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

    

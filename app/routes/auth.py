from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.models.user import Users
from app.database import get_db
from app.utils.encryption import hash_pwd
from app.schemas.user import login_user_PyModel
from app.utils.encryption import verify_pwd


router = APIRouter(
    prefix="/v1/api/auth",
    tags=["Authentication"]
)

@router.get("/login")
def login(pcredentials: login_user_PyModel, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.email == pcredentials.email).first()
    
    # wrong email or password
    if not user or not verify_pwd(pcredentials, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid credentials"
        )
    
    # create JWT token
    # return token
    return {
        'status': status.HTTP_200_OK,
        'msg': "login successfull"
    }
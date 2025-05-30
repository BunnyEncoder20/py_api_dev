from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.models.user import Users
from app.database import get_db
from app.utils.encryption import hash_pwd
from app.schemas import user, response
from app.utils import encryption, oauth2


router = APIRouter(
    prefix="/v1/api/auth",
    tags=["Authentication"]
)

@router.get("/login", response_model=response.Token_Reponse_PyModel)
def login(pcred: user.login_user_PyModel, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.email == pcred.email).first()
    
    # wrong email or password
    if not user or not encryption.verify_pwd(pcred.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid credentials"
        )
    
    # create JWT token
    access_token = oauth2.create_access_token(data={
        'user_id': user.id,
        'email': user.email
    })
    
    # return token
    return {
        'status': status.HTTP_200_OK,
        'msg': 'login successfull',
        'token_type': 'bearer',
        'access_token': access_token
    }
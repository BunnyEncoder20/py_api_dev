from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import InvalidTokenError

from app.schemas.user import user_token_PyModel
from app.models.user import Users
from app.database import get_db
from app.config import settings

from datetime import datetime, timedelta

# Needed for the JWT
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
EXPIRATION_MINS = 60
oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRATION_MINS)
    to_encode.update({"exp": expire})

    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return access_token


def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    '''func to auth user and fetch user from database'''
    
    credentials_expection = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Could not validate credentials from token.',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    
    verified_token = verify_access_token(token, credentials_expection)
    
    # fetch user from the DB
    user = db.query(Users).filter(Users.id == verified_token.id).first()
    
    return user


def verify_access_token(token: str, credentials_expection):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        token_id: str = payload.get('user_id')
        token_email: EmailStr = payload.get('email')
        
        if not token_id or not token_email:
            raise credentials_expection

        token_data = user_token_PyModel(id=token_id)
        
    except InvalidTokenError:
        raise credentials_expection
    
    return token_data
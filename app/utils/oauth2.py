from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError

from app.schemas.user import user_token_PyModel

from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
load_dotenv()   # loading env variables

# Needed for the JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRATION_MINS = 30
oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=EXPIRATION_MINS)
    to_encode.update({"exp": expire})

    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return access_token


def get_current_user(token: str = Depends(oauth2_schema)):
    credentials_expection = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Could not validate credentials from token.',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    
    return verify_access_token(token, credentials_expection)

def verify_access_token(token: str, credentials_expection):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        
        token_id: str = payload.get(user_id)
        token_email: EmailStr = payload.get(email)
        
        if not token_id or not token_email:
            raise credentials_expection

        token_data = user_token_PyModel(id=token_id, email=token_email)
    
    except InvalidTokenError:
        raise credentials_expection
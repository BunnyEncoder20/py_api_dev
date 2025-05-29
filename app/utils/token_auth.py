import jwt
from jwt.exceptions import InvalidTokenError

from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
load_dotenv()   # loading env variables

# Needed for the JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRATION_MINS = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=EXPIRATION_MINS)
    to_encode.update({"exp": expire})

    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return access_token
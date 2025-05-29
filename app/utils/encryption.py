from passlib.context import CryptContext

# setting up hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pwd(password: str) -> str:
    return pwd_context.hash(password)     # hashing the password

def verify_pwd(entered_pwd: str, hashed_pwd: str) -> bool:
    return pwd_context.verify(entered_pwd, hashed_pwd)
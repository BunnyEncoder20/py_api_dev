from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.models.user import Users
from app.database import get_db
from app.schemas import user, response
from app.utils import encryption, oauth2


router = APIRouter(
    prefix="/v1/api/auth",
    tags=["Authentication"]
)

@router.get("/login", response_model=response.Token_Reponse_PyModel)
def login(pcred: user.Login_user_PyModel, db: Session = Depends(get_db)):
    """
    Authenticate a user and generate a JWT access token upon successful login.
    Args:
        pcred (user.login_user_PyModel): The login credentials provided by the user, including email and password.
        db (Session, optional): SQLAlchemy database session dependency.
    Raises:
        HTTPException: If the provided email or password is incorrect, raises a 403 Forbidden error with an "Invalid credentials" message.
    Returns:
        dict: A dictionary containing the HTTP status code, a success message, the token type, and the generated JWT access token.
    """

    user = db.query(Users).filter(Users.email == pcred.email).first()

    # wrong email or password
    if not user or not encryption.verify_pwd(pcred.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
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

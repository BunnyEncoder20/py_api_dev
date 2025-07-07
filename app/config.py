# pydantic
from pydantic_settings import BaseSettings

'''------------------------------------------------------------------'''

# for validation of env variables
class Settings(BaseSettings):

    # postgres DB env variables
    DATABASE: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    SQLALCHEMY_DATABASE_URL: str

    # JWT variables
    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = ".env"

settings = Settings()
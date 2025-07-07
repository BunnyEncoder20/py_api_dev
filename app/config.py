# pydantic
from pydantic_settings import BaseSettings

'''------------------------------------------------------------------'''

# for validation of env variables
class Settings(BaseSettings):

    # postgres DB env variables
    DATABASE_HOSTNAME: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_PORT: int

    # JWT variables
    SECRET_KEY: str
    ALGORITHM: str
    EXPIRATION_MINS: int

    class Config:
        env_file = ".env"

settings = Settings()
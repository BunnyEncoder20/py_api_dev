import os
import time
import psycopg2     # pgsql direct driver 
from psycopg2.extras import RealDictCursor

# cofig for env variables 
from app.config import settings
'''------------------------------------------------------------------'''


# Way 1: To connect to Postgres DB: usiung psycopg2
def get_db_connection():
    attempt = 1
    MAX_ATTEMPTS = 3

    while attempt <= MAX_ATTEMPTS:
        try:
            conn = psycopg2.connect(
                host=settings.DATABASE_HOSTNAME,
                database=settings.DATABASE_NAME,
                user=settings.DATABASE_USERNAME,
                password=settings.DATABASE_PASSWORD,
                cursor_factory=RealDictCursor
            )
            print("[Server] ✅ Database connection was successful!")
            return conn

        except Exception as error:
            print(f"[Error] Attempt {attempt}: {error}")
            if attempt == MAX_ATTEMPTS:
                print("[Critical] ❌ Could not connect to DB after multiple attempts. Aborting...")
                exit()
            else:
                print("[Server] 🔁 Retrying in 3 seconds...")
                time.sleep(3)
                attempt += 1



# Way 2: Using SqlAlchemy ORM
from sqlalchemy import create_engine        # Sqlalchemy is a ORM (abstract layer between FastAPI and PGSQL) but still needs a database driver
from sqlalchemy.orm import sessionmaker, declarative_base
DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
def get_db() :                                          
    db = SessionLocal()
    try:
        yield db    
    finally:
        db.close()
import os
import time
import psycopg2     # pgsql direct driver 
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
load_dotenv()   # loading env variables


# Way 1: To connect to Postgres DB: usiung psycopg2
def get_db_connection():
    attempt = 1
    MAX_ATTEMPTS = 3

    while attempt <= MAX_ATTEMPTS:
        try:
            DB_NAME = os.getenv("DATABASE")
            DB_USER = os.getenv("DATABASE_USER")
            DB_PWD = os.getenv("DATABASE_PWD")

            conn = psycopg2.connect(
                host='localhost',
                database=DB_NAME,
                user=DB_USER,
                password=DB_PWD,
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
DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
from sqlalchemy import Column, Integer, String, Boolean, ARRAY, Text, TIMESTAMP
from sqlalchemy.sql import func
'''-----------------------'''
from ..database import Base

class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=False), server_default=func.now(), nullable=False)
from sqlalchemy import Column, Integer, String, Boolean, ARRAY, Text, TIMESTAMP
from sqlalchemy.sql import expression, func
'''-----------------------'''
from .database import Base

class Posts(Base):
    __tablename__ = "posts_table_v2"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default=expression.true())        # by default nullable = True
    tags = Column(ARRAY(Text), server_default="{}")
    created_at = Column(TIMESTAMP(timezone=False), server_default=func.now(), nullable=False)
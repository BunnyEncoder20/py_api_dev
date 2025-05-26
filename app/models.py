from sqlalchemy import Column, Integer, String, Boolean
'''-----------------------'''
from .database import Base

class Posts(Base):
    __tablename__ = "posts_table_v2"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)    
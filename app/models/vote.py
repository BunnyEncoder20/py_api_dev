from app.database import Base
from sqlalchemy import Column, Integer, ForeignKey

class Votes(Base):
    __tablename__ = "votes_table"

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    post_id = Column(Integer, ForeignKey('posts_table_v2.id', ondelete='CASCADE'), primary_key=True)
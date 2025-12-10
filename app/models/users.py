from sqlalchemy import Column, Integer, String, DateTime, LargeBinary
from app.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=False)
    email = Column(String, index=True, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
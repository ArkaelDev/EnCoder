from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, unique=True, nullable=False)
    email = Column(String, index=True, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)

    files = relationship("File", back_populates="owner") #this binds with files models

class UserInDB(User):
    hashed_password: str

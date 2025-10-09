from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, LargeBinary
from database import Base

'''Pretty self explanatory, we need a model for our orm. We copy the same model on main.py
but we add the table name'''

class Files(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, index=True, nullable=False)
    date_time =Column(DateTime, nullable=False)
    size = Column(Integer,nullable=False)
    type = Column(String, nullable=False)
    body = Column(LargeBinary, nullable=False)

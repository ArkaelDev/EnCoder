from sqlalchemy import Column, Integer, String, DateTime, LargeBinary
from app.database import Base

#Our orm model for files.

class Files(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, index=True, nullable=False)
    date_time =Column(DateTime, nullable=False)
    size = Column(Integer,nullable=False)
    type = Column(String, nullable=False)
    body = Column(LargeBinary, nullable=False)

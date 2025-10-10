from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, LargeBinary
from database import Base

#Our orm model.

class Files(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, index=True, nullable=False)
    date_time =Column(DateTime, nullable=False)
    size = Column(Integer,nullable=False)
    type = Column(String, nullable=False)
    body = Column(LargeBinary, nullable=False)

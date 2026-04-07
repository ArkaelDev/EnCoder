from sqlalchemy import Column, DateTime, ForeignKey, Integer, LargeBinary, String
from sqlalchemy.orm import relationship

from app.database import Base

# Our orm model for files.


class Files(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, index=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    date_time = Column(DateTime, nullable=False)
    size = Column(Integer, nullable=False)
    type = Column(String, nullable=False)
    body = Column(LargeBinary, nullable=False)

    owner = relationship(
        "User", back_populates="files"
    )  # this connects the fields between models

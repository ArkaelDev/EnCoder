from pydantic import BaseModel
from datetime import datetime

class File(BaseModel):
    file_name : str
    date_time: datetime
    size: int
    type: str

class FileCreate(File):
    body: bytes

class FileResponse(File):
    id: int


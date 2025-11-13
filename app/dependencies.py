from typing import List, Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from app.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''This is the connection to the database, notice that our "db" is SessionLocal -see line12 in database.py-
We use try in case it fails and always close the database after the operation'''


db_dependency = Annotated[Session, Depends(get_db)]
'''We create out dependency. This is useful in order to separate the logic, not repeating code and make easier refactorization'''
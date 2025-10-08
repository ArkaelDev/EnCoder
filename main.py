from fastapi import FastAPI, status, HTTPException, Depends, UploadFile, File, Form
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import List, Annotated
from pydantic import BaseModel
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
'''whit this we create all the tables and columns on the postgres database'''

class Files(BaseModel):
    name: str
    date : datetime
    body : bytes
'''we define our pydantic model for the files (is not named File because it interferes with File imported from fastapi -see line1-)
This class inherits from BaseModel.'''

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

@app.get("/")
async def root(status_code=status.HTTP_200_OK):
    '''Default route, only use is to know if the server is running'''
    return {"message": "Service is running, please log in"}

@app.post("/upload/")
async def upload_file(file: Files, db: db_dependency):
    '''
    We take the information received on json (as our pydantic model). Make the relation with the orm model.
    Then we try to add and commit those changes into our db.

    Args:
        file: Files (Information as pydantic model)
        db: db_dependency (Our connection to the database)
    Returns:
        Status code 201 if the contents are uploaded. Status code 500 if exception is raised.
        Status code 400 if the contents are not vali (Pydantic sends it by default)
    '''
    db_file = models.Files(
        file_name=file.name,
        date_time=file.date,
        body=file.body
    )
    try:
        db.add(db_file)
        db.commit()
        db.refresh(db_file)
    except SQLAlchemyError as e:
        db.rollback()
        return JSONResponse(content={"message":"Error saving file into the database."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        db.rollback()
        return JSONResponse(content={"message":"Unexpected error."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return JSONResponse(content={"message": "File uploaded successfully"}, status_code=status.HTTP_201_CREATED)

from fastapi import FastAPI, status, HTTPException, Depends, UploadFile, File, Form
from fastapi.responses import JSONResponse, Response
from datetime import datetime
from typing import List, Annotated
from pydantic import BaseModel
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

allowed_types = [
    "text/plain",
    "text/html",
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/msword",
    "application/rtf",
    "application/vnd.oasis.opendocument.spreadsheet",
    "application/vnd.ms-excel",
    "application/epub+zip"
]
'''Only acepting text like files'''
app = FastAPI()
models.Base.metadata.create_all(bind=engine)
'''whit this we create all the tables and columns on the postgres database'''


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

@app.post("/upload")
async def upload_file(uploaded_file: UploadFile, db: db_dependency):
    '''
    Summary:
        We take the file from the form, read its binaries. Make the relation with the orm model.
        We make sure that the file uploaded matches our allowed types. If not we raise an exception.
        Then we try to add and commit those changes into our db.

    Args:
        uploaded_file: UploadFile (The provided file)
        db: db_dependency (Our connection to the database)
    Returns:
        Status code 201 if the contents are uploaded. Status code 500 if exception is raised and show the error as detail.
    '''
    content = await uploaded_file.read()
    db_file = models.Files(
        file_name = uploaded_file.filename,
        date_time = datetime.now(),
        size = uploaded_file.size,
        type = uploaded_file.content_type,
        body = content
    )
    if uploaded_file.content_type in allowed_types:
        try:
            db.add(db_file)
            db.commit()
            db.refresh(db_file)
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        return JSONResponse(content={"message": "File uploaded successfully"}, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="File type not supported.")

@app.get("/files/{file_id}")
async def get_item(file_id: int, db: db_dependency):
    '''
    Summary:
        We use our file id to search in our database through the model. Raise an exception if any error occurs, show the error.
        Raise and exception if the file doesn't exists.
    Args:
        file_id: int (The primary key of the file. Declared as int for automatic validation)
        db: db_dependency (Our connection to the database)
    Returns:
        The content as bytes. MIMI type for reading purposes.
        Headers content-disposition attachment so we suggest that the file is downloaded with the same name as in the database.

    '''
    try:
        file = db.get(models.Files, file_id)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    return Response(
        content = file.body,
        media_type= file.type,
        headers={"Content-Disposition": f'attachment; filename="{file.file_name}"'})
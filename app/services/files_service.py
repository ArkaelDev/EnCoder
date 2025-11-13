from app.models.files import Files
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from app.logger import logger
from app.dependencies import db_dependency
from fastapi import HTTPException, status, UploadFile
from app.dependencies import db_dependency
from fastapi.responses import JSONResponse

allowed_types = [
    #Only text like files.
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


async def get_file_by_id(file_id: int, db):
    '''Summary:
        We use our file id to search in our database through the model. Raise an exception if any error occurs, show the error.
        Raise and exception if the file doesn't exists.
    Args:
        file_id: int (The primary key of the file. Declared as int for automatic validation)
        db: db_dependency (Our connection to the database)
    Returns:
        The content as bytes. MIMI type for reading purposes.
        Headers content-disposition attachment so we suggest that the file is downloaded with the same name as in the database.'''
    try:
        file = db.get(Files, file_id)
    except SQLAlchemyError as e:
        logger.exception(msg = e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    if not file:
        logger.exception(msg = "File not found.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NO")
    return file
    

async def upload_file_service(uploaded_file: UploadFile, db: db_dependency):
    '''Summary:
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
    db_file = Files(
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
            logger.exception(msg = e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        except Exception as e:
            db.rollback()
            logger.exception(msg = e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        return JSONResponse(content={"message": "File uploaded successfully"}, status_code=status.HTTP_201_CREATED)
    else:
        logger.error(msg= "File type not supported.")
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="File type not supported.")
    
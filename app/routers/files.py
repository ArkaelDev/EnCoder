from fastapi import APIRouter, UploadFile
from fastapi.responses import  Response
from app.dependencies import db_dependency
from app.services.files_service import get_file_by_id, upload_file_service


router = APIRouter()

@router.post("/upload")
async def upload_file(uploaded_file: UploadFile, db: db_dependency):
    return await upload_file_service(uploaded_file, db)


@router.get("/files/{file_id}")
async def get_item(file_id: int, db: db_dependency):
    file = await get_file_by_id(file_id, db)
    return Response(
        content = file.body,
        media_type= file.type,
        headers={"Content-Disposition": f'attachment; filename="{file.file_name}"'})
from fastapi import APIRouter, UploadFile
from fastapi.param_functions import Depends
from fastapi.responses import Response

from app.core.security import get_current_active_user
from app.dependencies import db_dependency
from app.schemas.files import FileCreate, FileResponse
from app.services.files_service import get_file_by_id, upload_file_service

router = APIRouter()


@router.post("/upload", response_model=FileCreate)
async def upload_file(
    uploaded_file: UploadFile,
    db: db_dependency,
    current_user: User = Depends(get_current_active_user),
):
    return await upload_file_service(uploaded_file, db)


@router.get("/files/{file_id}", response_model=FileResponse)
async def get_item(file_id: int, db: db_dependency):
    file = await get_file_by_id(file_id, db)
    return Response(
        content=file.body,
        media_type=file.type,
        headers={"Content-Disposition": f'attachment; filename="{file.file_name}"'},
    )

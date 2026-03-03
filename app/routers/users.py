from fastapi import APIRouter
from fastapi.responses import  Response
from app.dependencies import db_dependency
from app.services.users_service import create_user
from app.schemas.users import UserIn, UserOut, UserInDB
from app.models.users import User

router = APIRouter()

@router.post("/create_user", response_model= UserIn)
async def create_users(CreatedUser: UserIn, db: db_dependency):
    return await create_user(CreatedUser, db)

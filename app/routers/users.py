from fastapi import APIRouter, Depends
from fastapi.responses import  Response
from app.dependencies import db_dependency
from app.services.users_service import create_user
from app.schemas.users import UserIn, UserOut, UserInDB
from typing import Annotated
from app.core.security import get_current_active_user


router = APIRouter()

@router.post("/create_user", response_model= UserIn)
async def create_users(CreatedUser: UserIn, db: db_dependency):
    return await create_user(CreatedUser, db)

@router.get("/users/me/")
async def read_users_me(
    current_user: Annotated[UserIn, Depends(get_current_active_user)],
) -> UserIn:
    return current_user

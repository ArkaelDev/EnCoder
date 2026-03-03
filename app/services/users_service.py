from app.models.users import User
from app.schemas.users import UserIn
from app.logger import logger
from sqlalchemy.exc import SQLAlchemyError
from app.dependencies import db_dependency
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from app.utils.hash_utils import get_password_hash
from app.models.users import UserInDB
from pwdlib import PasswordHash
from app.utils.hash_utils import password_hash


async def create_user(CreatedUser : UserIn, db : db_dependency):

    db_user = User(username = CreatedUser.username,
                   email = CreatedUser.email,
                   password = get_password_hash(CreatedUser.password),
                   full_name = CreatedUser.full_name
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except SQLAlchemyError as e:
        db.rollback()
        logger.exception(msg = e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        db.rollback()
        logger.exception(msg = e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return JSONResponse(content={"message": "User created successfully"}, status_code=status.HTTP_201_CREATED)

async def get_user(db: db_dependency, username: str):
    if username in db:
        user_dict =db[username]
        return UserInDB(**user_dict)

async def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_hash.hash(password)

async def authenticate_user(db: db_dependency, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
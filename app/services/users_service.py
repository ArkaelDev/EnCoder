from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.dependencies import db_dependency
from app.logger import logger
from app.models.users import User
from app.schemas.users import UserIn
from app.utils.hash_utils import DUMMY_HASH, get_password_hash, verify_password


async def create_user(CreatedUser: UserIn, db: db_dependency):

    db_user = User(
        username=CreatedUser.username,
        email=CreatedUser.email,
        password=get_password_hash(CreatedUser.password),
        full_name=CreatedUser.full_name,
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except SQLAlchemyError as e:
        db.rollback()
        logger.exception(msg=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    except Exception as e:
        db.rollback()
        logger.exception(msg=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    return JSONResponse(
        content={"message": "User created successfully"},
        status_code=status.HTTP_201_CREATED,
    )


def get_user(db, username: str):
    query = select(User).where(User.username == username)
    result = db.execute(query)
    return result.scalar_one_or_none()


async def authenticate_user(db: db_dependency, username: str, password: str):
    user = get_user(db, username)
    if not user:
        verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(password, user.password):
        return False
    return user

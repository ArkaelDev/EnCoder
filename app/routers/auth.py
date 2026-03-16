from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from app.core.security import Token, create_access_token
from app.services.users_service import authenticate_user
from app.dependencies import db_dependency
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from app.core.settings import ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter()

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
) -> Token:
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
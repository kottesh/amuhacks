from typing import Any, Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm 
from sqlalchemy.ext.asyncio import AsyncSession

import crud, schemas
from core import security
from db.base import get_session
from jose import JWTError

from datetime import datetime, timezone

router = APIRouter()

@router.post("/login", response_model=schemas.Token)
async def login(
    db: Annotated[AsyncSession, Depends(get_session)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()] 
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    Uses form data (username = email, password).
    """
    user = await crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

    access_token = security.create_access_token(user.email) # Use email as subject
    refresh_token = security.create_refresh_token(user.email)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

@router.post("/register", response_model=schemas.User)
async def register_user(
    *,
    db: Annotated[AsyncSession, Depends(get_session)],
    user_in: schemas.UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = await crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system.",
        )
    user = await crud.user.create(db, obj_in=user_in)
    return user


@router.post("/refresh", response_model=schemas.Token)
async def refresh_access_token(
    refresh_token: Annotated[str, Body(embed=True)], # Expect {"refresh_token": "..."}
    db: Annotated[AsyncSession, Depends(get_session)]
) -> Any:
    """
    Refresh the access token using a valid refresh token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = security.decode_token(refresh_token)
        if payload is None:
            raise credentials_exception
        token_data = schemas.TokenPayload(**payload)
        if token_data.sub is None:
            raise credentials_exception
        if datetime.fromtimestamp(payload.get('exp', 0), tz=timezone.utc) < datetime.now(timezone.utc):
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except JWTError:
        raise credentials_exception

    user = await crud.user.get_by_email(db, email=token_data.sub)

    if user is None or not user.is_active:
        raise credentials_exception

    new_access_token = security.create_access_token(user.email)
    new_refresh_token = security.create_refresh_token(user.email)

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token, # send back the new refresh token
        "token_type": "bearer",
    }



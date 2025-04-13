from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

import crud, schemas
from db import models
from api.v1 import deps
from db.base import get_session

router = APIRouter()

@router.post("/", response_model=schemas.Account, status_code=status.HTTP_201_CREATED)
async def create_account(
    *,
    db: Annotated[AsyncSession, Depends(get_session)],
    account_in: schemas.AccountCreate,
    current_user: Annotated[models.User, Depends(deps.get_current_active_user)]
):
    """
    Create a new financial account for the current user.
    Initial balance defaults to 0 unless specified in account_in.
    """
    account = await crud.account.create_with_owner(
        db=db, obj_in=account_in, owner_id=current_user.id
    )
    return account

@router.get("/", response_model=List[schemas.Account])
async def read_accounts(
    *,
    db: Annotated[AsyncSession, Depends(get_session)],
    skip: int = 0,
    limit: int = 100,
    current_user: Annotated[models.User, Depends(deps.get_current_active_user)]
):
    """
    Retrieve all financial accounts for the current user.
    """
    accounts = await crud.account.get_multi_by_owner(
        db=db, owner_id=current_user.id, skip=skip, limit=limit
    )
    return accounts

@router.get("/{account_id}", response_model=schemas.Account)
async def read_account(
    *,
    db: Annotated[AsyncSession, Depends(get_session)],
    account_id: int,
    current_user: Annotated[models.User, Depends(deps.get_current_active_user)]
):
    """
    Get a specific account by ID.
    """
    account = await crud.account.get_by_owner(db=db, id=account_id, owner_id=current_user.id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return account

@router.put("/{account_id}", response_model=schemas.Account)
async def update_account(
    *,
    db: Annotated[AsyncSession, Depends(get_session)],
    account_id: int,
    account_in: schemas.AccountUpdate,
    current_user: Annotated[models.User, Depends(deps.get_current_active_user)]
):
    """
    Update an existing account.
    Note: Updating balance directly via this endpoint might be discouraged;
    prefer updates via transactions.
    """
    account = await crud.account.get_by_owner(db=db, id=account_id, owner_id=current_user.id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

    # Prevent direct balance updates if needed, or log them carefully
    if account_in.balance is not None and account_in.balance != account.balance:
         # Consider raising an error or adding specific permissions for direct balance changes
         print(f"Warning: Direct balance update attempt on account {account_id} by user {current_user.id}")
         # For now, allow it as per schema, but be aware of implications.

    account = await crud.account.update(db=db, db_obj=account, obj_in=account_in)
    return account

@router.delete("/{account_id}", response_model=schemas.Account)
async def delete_account(
    *,
    db: Annotated[AsyncSession, Depends(get_session)],
    account_id: int,
    current_user: Annotated[models.User, Depends(deps.get_current_active_user)]
):
    """
    Delete an account.
    Ensure cascading deletes are handled correctly in the database model
    for associated transactions if that's the desired behavior.
    """
    account = await crud.account.get_by_owner(db=db, id=account_id, owner_id=current_user.id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

    deleted_account = await crud.account.remove(db=db, id=account_id)
    return deleted_account 

import logging
from typing import List, Annotated, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession

import crud, schemas
from db import models
from api.v1 import deps
from db.base import get_session
from services import nlp_parser

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/parse", response_model=list[schemas.NlpParsedTransaction])
async def parse_natural_language_transaction(
    nlp_input: schemas.NlpInput,
    current_user: Annotated[models.User, Depends(deps.get_current_active_user)],
) -> list[schemas.NlpParsedTransaction]:
    """
    Takes natural language text and returns structured transaction data using LLM.

    This endpoint **does not** save the transaction. It's intended for the frontend
    to display the parsed result for user confirmation or editing before calling
    the `POST /transactions/` endpoint.
    """
    logger.info(f"User {current_user.email} parsing text: '{nlp_input.text}'")
    parsed_data = await nlp_parser.parse_transaction_nlp(text=nlp_input.text)

    if not parsed_data:
        logger.warning(f"NLP parsing failed for text: '{nlp_input.text}'")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not parse transaction details from the provided text. The LLM might have failed or returned invalid/unparsable data."
        )

    logger.info(f"NLP parsing successful for user {current_user.email}. Result: {parsed_data}")
    return parsed_data


@router.post("/", response_model=schemas.Transaction, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    *,
    db: Annotated[AsyncSession, Depends(get_session)],
    transaction_in: schemas.TransactionCreate,
    current_user: Annotated[models.User, Depends(deps.get_current_active_user)],
):
    """
    Creates a new transaction in the database after user confirmation/input.
    Atomically updates the associated account balance.
    """
    logger.info(f"User {current_user.email} creating transaction for account {transaction_in.account_id}")
    account = await crud.account.get_by_owner(db=db, id=transaction_in.account_id, owner_id=current_user.id)
    if not account:
        logger.warning(f"User {current_user.email} attempted to create transaction for non-owned/non-existent account {transaction_in.account_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found or does not belong to the current user."
        )

    try:
        transaction = await crud.transaction.create_with_owner(
            db=db, obj_in=transaction_in, owner_id=current_user.id
        )
        logger.info(f"Transaction {transaction.id} created successfully for user {current_user.email}")
        return transaction
    except ValueError as e:
        logger.error(f"Error creating transaction for user {current_user.email}: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error creating transaction for user {current_user.email}: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error creating transaction.")


@router.get("/", response_model=List[schemas.Transaction])
async def read_transactions(
    db: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[models.User, Depends(deps.get_current_active_user)],
    skip: int = 0,
    limit: int = 100,
    account_id: Optional[int] = Query(None, description="Filter by account ID"),
    start_date: Optional[datetime] = Query(None, description="Filter by start date (YYYY-MM-DDTHH:MM:SS)"),
    end_date: Optional[datetime] = Query(None, description="Filter by end date (YYYY-MM-DDTHH:MM:SS)"),
    category: Optional[str] = Query(None, description="Filter by category (case-insensitive, partial match)"),
    transaction_type: Optional[schemas.TransactionType] = Query(None, alias="type", description="Filter by transaction type (INCOME or EXPENSE)"),
):
    """
    Retrieve transactions for the current user, with optional filtering.
    """
    logger.info(f"User {current_user.email} reading transactions with filters: account={account_id}, start={start_date}, end={end_date}, cat={category}, type={transaction_type}")
    transactions = await crud.transaction.get_multi_by_owner_and_account(
        db=db,
        owner_id=current_user.id,
        account_id=account_id,
        skip=skip,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
        category=category,
        transaction_type=transaction_type,
    )
    return transactions

@router.get("/{transaction_id}", response_model=schemas.Transaction)
async def read_transaction(
    *,
    db: Annotated[AsyncSession, Depends(get_session)],
    transaction_id: int,
    current_user: Annotated[models.User, Depends(deps.get_current_active_user)],
):
    """
    Get a specific transaction by ID.
    """
    logger.info(f"User {current_user.email} reading transaction {transaction_id}")
    transaction = await crud.transaction.get_by_owner(db=db, id=transaction_id, owner_id=current_user.id)
    if not transaction:
        logger.warning(f"User {current_user.email} failed to find transaction {transaction_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return transaction

@router.put("/{transaction_id}", response_model=schemas.Transaction)
async def update_transaction(
    *,
    db: Annotated[AsyncSession, Depends(get_session)],
    transaction_id: int,
    transaction_in: schemas.TransactionUpdate,
    current_user: Annotated[models.User, Depends(deps.get_current_active_user)],
):
    """
    Update a transaction. Atomically adjusts account balances if amount,
    type, or account association changes.
    """
    logger.info(f"User {current_user.email} updating transaction {transaction_id}")

    db_transaction = await crud.transaction.get_by_owner(db=db, id=transaction_id, owner_id=current_user.id)
    if not db_transaction:
        logger.warning(f"User {current_user.email} failed to find transaction {transaction_id} for update")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")

    if transaction_in.account_id is not None and transaction_in.account_id != db_transaction.account_id:
        new_account = await crud.account.get_by_owner(db=db, id=transaction_in.account_id, owner_id=current_user.id)
        if not new_account:
             logger.warning(f"User {current_user.email} attempted update transaction {transaction_id} to non-owned/non-existent account {transaction_in.account_id}")
             raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="New target account not found or does not belong to the current user."
            )

    try:
        updated_transaction = await crud.transaction.update_transaction_and_balance(
            db=db, db_obj=db_transaction, obj_in=transaction_in
        )

        logger.info(f"Transaction {transaction_id} updated successfully for user {current_user.email}")
        return updated_transaction
    except ValueError as e:
        logger.error(f"Error updating transaction {transaction_id} for user {current_user.email}: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error updating transaction {transaction_id} for user {current_user.email}: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error updating transaction.")


@router.delete("/{transaction_id}", response_model=schemas.Transaction)
async def delete_transaction(
    *,
    db: Annotated[AsyncSession, Depends(get_session)],
    transaction_id: int,
    current_user: Annotated[models.User, Depends(deps.get_current_active_user)],
):
    """
    Delete a transaction. Atomically reverts the transaction's effect
    on the associated account balance.
    """
    logger.info(f"User {current_user.email} deleting transaction {transaction_id}")
    try:
        deleted_transaction = await crud.transaction.remove_transaction_and_balance(
            db=db, id=transaction_id, owner_id=current_user.id
        )
        if not deleted_transaction:
            logger.warning(f"User {current_user.email} failed to find transaction {transaction_id} for deletion")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")

        logger.info(f"Transaction {transaction_id} deleted successfully for user {current_user.email}")
        return deleted_transaction
    except ValueError as e:
        logger.error(f"Error deleting transaction {transaction_id} for user {current_user.email}: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error deleting transaction {transaction_id} for user {current_user.email}: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error deleting transaction.")


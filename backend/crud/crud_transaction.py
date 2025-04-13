from typing import List, Optional
from sqlalchemy import select, delete as sqlalchemy_delete
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from db.models import Transaction, Account
from schemas.transaction import TransactionCreate, TransactionUpdate, TransactionType
from .crud_account import account as crud_account 

from datetime import datetime

class CRUDTransaction(CRUDBase[Transaction, TransactionCreate, TransactionUpdate]):
    """CRUD operations for Transaction model."""

    async def create_with_owner(
        self, db: AsyncSession, *, obj_in: TransactionCreate, owner_id: int
    ) -> Transaction:
        """
        Create a new transaction, link to owner, and update account balance atomically.
        """

        amount_change = obj_in.amount if obj_in.type == TransactionType.INCOME else -obj_in.amount
        updated_account = await crud_account.update_balance(
            db=db,
            account_id=obj_in.account_id,
            amount_change=amount_change
        )

        if not updated_account:
            raise ValueError(f"Account with id {obj_in.account_id} not found for balance update.")

        # Create Transaction Record directly from the Pydantic model fields
        db_obj = self.model(
            amount=obj_in.amount,
            type=obj_in.type,
            category=obj_in.category,
            date=obj_in.date,  # This will now be a proper `datetime.datetime` object
            description=obj_in.description,
            account_id=obj_in.account_id,
            owner_id=owner_id
        )

        db.add(db_obj)
        await db.flush()
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_multi_by_owner_and_account(
        self,
        db: AsyncSession,
        *,
        owner_id: int,
        account_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        category: Optional[str] = None,
        transaction_type: Optional[TransactionType] = None,
    ) -> List[Transaction]:
        """Get multiple transactions for an owner, optionally filtered by account and other criteria."""
        query = select(self.model).filter(Transaction.owner_id == owner_id)

        if account_id is not None:
            query = query.filter(Transaction.account_id == account_id)
        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            from datetime import timedelta
            query = query.filter(Transaction.date < end_date + timedelta(days=1))
        if category:
            query = query.filter(Transaction.category.ilike(f"%{category}%")) # Case-insensitive search
        if transaction_type:
            query = query.filter(Transaction.type == transaction_type)


        query = query.order_by(self.model.date.desc()).offset(skip).limit(limit) # Order by date descending
        result = await db.execute(query)
        return result.scalars().all()

    async def get_by_owner(
        self, db: AsyncSession, *, owner_id: int, id: int
    ) -> Optional[Transaction]:
        """Get a single transaction by ID, ensuring it belongs to the owner."""
        result = await db.execute(
            select(self.model).filter(Transaction.id == id, Transaction.owner_id == owner_id)
        )
        return result.scalars().first()

    async def update_transaction_and_balance(
        self,
        db: AsyncSession,
        *,
        db_obj: Transaction,
        obj_in: TransactionUpdate
    ) -> Optional[Transaction]:
        """
        Update a transaction and adjust account balances accordingly.
        Handles changes in amount, type, and account_id.
        """

        from fastapi.encoders import jsonable_encoder
        update_data = obj_in.dict(exclude_unset=True)

        original_amount_effect = db_obj.amount if db_obj.type == TransactionType.INCOME else -db_obj.amount
        new_amount = update_data.get("amount", db_obj.amount)
        new_type = update_data.get("type", db_obj.type)
        new_account_id = update_data.get("account_id", db_obj.account_id)
        new_amount_effect = new_amount if new_type == TransactionType.INCOME else -new_amount

        account_changed = new_account_id != db_obj.account_id
        amount_or_type_changed = new_amount_effect != original_amount_effect

        if account_changed:
            old_account_update = await crud_account.update_balance(db=db, account_id=db_obj.account_id, amount_change=-original_amount_effect)
            if not old_account_update: raise ValueError("Original account not found during update.")
            new_account_update = await crud_account.update_balance(db=db, account_id=new_account_id, amount_change=new_amount_effect)
            if not new_account_update: raise ValueError("New account not found during update.")
        elif amount_or_type_changed:
            balance_diff = new_amount_effect - original_amount_effect
            account_update = await crud_account.update_balance(db=db, account_id=db_obj.account_id, amount_change=balance_diff)
            if not account_update: raise ValueError("Account not found during update.")

        for field in jsonable_encoder(db_obj):
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj


    async def remove_transaction_and_balance(
        self, db: AsyncSession, *, id: int, owner_id: int
    ) -> Optional[Transaction]:
        """
        Remove a transaction by ID and revert its effect on the account balance.
        Ensures the transaction belongs to the owner.
        """

        transaction_to_delete = await self.get_by_owner(db=db, id=id, owner_id=owner_id)

        if not transaction_to_delete:
            return None

        amount_effect_to_revert = transaction_to_delete.amount if transaction_to_delete.type == TransactionType.INCOME else -transaction_to_delete.amount
        balance_change = -amount_effect_to_revert

        updated_account = await crud_account.update_balance(
            db=db,
            account_id=transaction_to_delete.account_id,
            amount_change=balance_change
        )

        if not updated_account:
            raise ValueError(f"Account with id {transaction_to_delete.account_id} not found for balance revert during delete.")

        await db.delete(transaction_to_delete)
        await db.flush()
        return transaction_to_delete 

transaction = CRUDTransaction(Transaction)

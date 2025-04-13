from typing import List, Optional
from sqlalchemy import select, update as sqlalchemy_update, delete as sqlalchemy_delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from crud.base import CRUDBase
from db.models import Account
from schemas.account import AccountCreate, AccountUpdate

class CRUDAccount(CRUDBase[Account, AccountCreate, AccountUpdate]):
    """CRUD operations for Account model."""

    async def create_with_owner(
        self, db: AsyncSession, *, obj_in: AccountCreate, owner_id: int
    ) -> Account:
        """Create a new account linked to an owner."""

        from fastapi.encoders import jsonable_encoder

        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_multi_by_owner(
        self, db: AsyncSession, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Account]:
        """Get multiple accounts belonging to a specific owner."""
        result = await db.execute(
            select(self.model)
            .filter(Account.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .order_by(self.model.name)
        )
        return result.scalars().all()

    async def get_by_owner(
        self, db: AsyncSession, *, owner_id: int, id: int
    ) -> Optional[Account]:
        """Get a single account by ID, ensuring it belongs to the owner."""
        result = await db.execute(
            select(self.model).filter(Account.id == id, Account.owner_id == owner_id)
        )
        return result.scalars().first()

    async def update_balance(
        self, db: AsyncSession, *, account_id: int, amount_change: float
    ) -> Optional[Account]:
        """
        Atomically update the balance of an account.
        Use amount_change > 0 for income/increase, < 0 for expense/decrease.
        Uses SELECT FOR UPDATE to lock the row during the transaction.
        """
        result = await db.execute(
            select(self.model)
            .filter(self.model.id == account_id)
            .with_for_update()
        )
        account = result.scalars().first()

        if not account:
            return None

        new_balance = account.balance + amount_change
        await db.execute(
            sqlalchemy_update(self.model)
            .where(self.model.id == account_id)
            .values(balance=new_balance)
        )
        account.balance = new_balance
        return account

account = CRUDAccount(Account)

from typing import Any, Dict, Optional, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import get_password_hash, verify_password
from crud.base import CRUDBase
from db.models import User
from schemas.user import UserCreate, UserUpdate

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """CRUD operations for User model."""

    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        """Get a user by email."""
        result = await db.execute(select(self.model).filter(self.model.email == email))
        return result.scalars().first()

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        """Create a new user, hashing the password."""
        create_data = obj_in.dict(exclude={"password"})
        create_data["hashed_password"] = get_password_hash(obj_in.password)

        db_obj = self.model(**create_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: User,
        obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        """Update a user, hashing the password if provided."""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        if "password" in update_data and update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            update_data["hashed_password"] = hashed_password
            del update_data["password"] 
        elif "password" in update_data:
             del update_data["password"] 

        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def authenticate(
        self, db: AsyncSession, *, email: str, password: str
    ) -> Optional[User]:
        """Authenticate a user by email and password."""
        user = await self.get_by_email(db, email=email)
        if not user:
            return None
        if not user.is_active: 
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

user = CRUDUser(User)

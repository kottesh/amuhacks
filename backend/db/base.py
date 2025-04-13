from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

from core.config import settings
from .base_class import Base

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=True,
)

AsyncSessionFactory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency to get an async database session.
    Ensures the session is closed after the request.
    """
    async with AsyncSessionFactory() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


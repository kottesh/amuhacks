from sqlalchemy import Column, Integer, String, Float, DateTime, Enum as SQLEnum, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum 

from .base_class import Base 
from schemas.transaction import TransactionType as TransactionTypeEnum

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    accounts = relationship("Account", back_populates="owner", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="owner", cascade="all, delete-orphan")

class Account(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    type = Column(String, nullable=False) 
    balance = Column(Float, default=0.0, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account", cascade="all, delete-orphan")

class Transaction(Base):
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    type = Column(SQLEnum(TransactionTypeEnum, name="transaction_type_enum"), nullable=False, index=True)
    category = Column(String, index=True, nullable=True) 
    date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    description = Column(String, nullable=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False) 

    account = relationship("Account", back_populates="transactions")
    owner = relationship("User", back_populates="transactions")

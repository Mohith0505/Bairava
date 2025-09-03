# backend/app/domain/models/trading.py
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, func
from app.infra.db import Base

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    # For now we keep single-user; we’ll wire multi-user auth later with user_id
    broker = Column(String, nullable=False, default="paper")  # "paper" or real broker key
    label = Column(String, nullable=False, default="Default")
    enabled = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, nullable=False)
    symbol = Column(String, nullable=False)
    side = Column(String, nullable=False)  # "BUY" / "SELL"
    qty = Column(Integer, nullable=False)
    price = Column(Float, nullable=True)   # None => market (we'll fill with 100.0)
    status = Column(String, nullable=False, default="NEW")  # NEW/FILLED/CANCELED
    created_at = Column(DateTime, server_default=func.now())

class Position(Base):
    __tablename__ = "positions"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, nullable=False)
    symbol = Column(String, nullable=False)
    qty = Column(Integer, nullable=False, default=0)
    avg_price = Column(Float, nullable=False, default=0.0)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

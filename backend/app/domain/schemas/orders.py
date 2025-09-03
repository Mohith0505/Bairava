# backend/app/domain/schemas/orders.py
from pydantic import BaseModel, Field
from typing import Optional, Literal

Side = Literal["BUY", "SELL"]

class OrderCreate(BaseModel):
    account_id: int
    symbol: str
    side: Side
    qty: int = Field(gt=0)
    price: Optional[float] = None  # None => market

class OrderOut(BaseModel):
    id: int
    account_id: int
    symbol: str
    side: Side
    qty: int
    price: Optional[float]
    status: str

    class Config:
        from_attributes = True

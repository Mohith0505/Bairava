# backend/app/domain/schemas/accounts.py
from pydantic import BaseModel

class AccountCreate(BaseModel):
    broker: str = "paper"
    label: str = "Default"

class AccountOut(BaseModel):
    id: int
    broker: str
    label: str
    enabled: bool

    class Config:
        from_attributes = True

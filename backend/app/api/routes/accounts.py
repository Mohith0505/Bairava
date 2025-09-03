# backend/app/api/routes/accounts.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from app.infra.db import get_db
from app.domain.models.trading import Account
from app.domain.schemas.accounts import AccountCreate, AccountOut

router = APIRouter()

@router.get("", response_model=List[AccountOut])
def list_accounts(db: Session = Depends(get_db)):
    q = db.execute(select(Account).order_by(Account.id))
    return q.scalars().all()

@router.post("", response_model=AccountOut, status_code=status.HTTP_201_CREATED)
def create_account(payload: AccountCreate, db: Session = Depends(get_db)):
    acc = Account(broker=payload.broker, label=payload.label, enabled=True)
    db.add(acc)
    db.commit()
    db.refresh(acc)
    return acc

@router.patch("/{account_id}", response_model=AccountOut)
def update_account(account_id: int, payload: AccountCreate, db: Session = Depends(get_db)):
    acc = db.get(Account, account_id)
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    acc.broker = payload.broker or acc.broker
    acc.label = payload.label or acc.label
    db.commit()
    db.refresh(acc)
    return acc

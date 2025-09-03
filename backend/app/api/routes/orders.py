# backend/app/api/routes/orders.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional

from app.infra.db import get_db
from app.domain.models.trading import Account, Order
from app.domain.schemas.orders import OrderCreate, OrderOut
from app.domain.services.paper import apply_fill

router = APIRouter()

def _account_or_400(db: Session, account_id: int) -> Account:
    acc = db.get(Account, account_id)
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    if not acc.enabled:
        raise HTTPException(status_code=400, detail="Account disabled")
    return acc

@router.get("", response_model=List[OrderOut])
def list_orders(db: Session = Depends(get_db)):
    q = db.execute(select(Order).order_by(Order.id.desc()))
    return q.scalars().all()

@router.get("/{order_id}", response_model=Optional[OrderOut])
def get_order(order_id: int, db: Session = Depends(get_db)):
    return db.get(Order, order_id)

@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    _account_or_400(db, payload.account_id)

    ord_obj = Order(
        account_id=payload.account_id,
        symbol=payload.symbol.upper().strip(),
        side=payload.side,
        qty=int(payload.qty),
        price=float(payload.price) if payload.price is not None else None,
        status="NEW",
    )
    db.add(ord_obj)
    db.flush()

    # Paper fill immediately
    fill_price = ord_obj.price if ord_obj.price is not None else 100.0
    apply_fill(db, ord_obj.account_id, ord_obj.symbol, ord_obj.side, ord_obj.qty, fill_price)

    ord_obj.status = "FILLED"
    db.commit()
    db.refresh(ord_obj)
    return ord_obj

@router.post("/{order_id}/cancel", response_model=OrderOut)
def cancel_order(order_id: int, db: Session = Depends(get_db)):
    o = db.get(Order, order_id)
    if not o:
        raise HTTPException(status_code=404, detail="Order not found")
    if o.status != "NEW":
        raise HTTPException(status_code=400, detail=f"Cannot cancel in status {o.status}")
    o.status = "CANCELED"
    db.commit()
    db.refresh(o)
    return o

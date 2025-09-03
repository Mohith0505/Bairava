# backend/app/api/routes/positions.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Dict

from app.infra.db import get_db
from app.domain.models.trading import Position

router = APIRouter()

def _to_out(p: Position) -> Dict:
    return {
        "id": p.id,
        "account_id": p.account_id,
        "symbol": p.symbol,
        "qty": p.qty,
        "avg_price": p.avg_price,
    }

@router.get("", response_model=List[dict])
def list_positions(db: Session = Depends(get_db)):
    q = db.execute(select(Position).order_by(Position.id))
    return [_to_out(p) for p in q.scalars().all()]

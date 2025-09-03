# backend/app/domain/services/paper.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.domain.models.trading import Position

def _get_pos(sess: Session, account_id: int, symbol: str) -> Position:
    pos = sess.execute(
        select(Position).where(
            Position.account_id == account_id,
            Position.symbol == symbol
        )
    ).scalar_one_or_none()
    if not pos:
        pos = Position(account_id=account_id, symbol=symbol, qty=0, avg_price=0.0)
        sess.add(pos)
        sess.flush()
    return pos

def apply_fill(sess: Session, account_id: int, symbol: str, side: str, qty: int, price: float) -> None:
    """
    Simple inventory model:
      - BUY increases qty; new avg = (old_qty*old_avg + qty*price) / (old_qty + qty)
      - SELL decreases qty; avg remains the same for remaining.
    No realized PnL tracking here (we’ll add Trades later).
    """
    pos = _get_pos(sess, account_id, symbol)
    if side.upper() == "BUY":
        new_qty = pos.qty + qty
        if new_qty <= 0:
            pos.qty = 0
            pos.avg_price = 0.0
        else:
            pos.avg_price = (pos.qty * pos.avg_price + qty * price) / new_qty
            pos.qty = new_qty
    else:  # SELL
        pos.qty = pos.qty - qty
        if pos.qty < 0:
            # allow going short; keep avg at entry price for short logic (simple)
            pos.avg_price = price
        if pos.qty == 0:
            pos.avg_price = 0.0
    sess.flush()

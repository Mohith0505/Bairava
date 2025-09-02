from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt, JWTError

from app.config import settings
from app.infra.db import get_db
from app.domain.models.user import User
from app.domain.schemas.auth import MeOut

router = APIRouter()

async def get_current_user(authorization: str = Header(None), db: AsyncSession = Depends(get_db)) -> User:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    token = authorization.split()[1]
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        sub = payload.get("sub")
        if not sub:
            raise HTTPException(status_code=401, detail="Invalid token")
        user_id = int(sub)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    res = await db.execute(select(User).where(User.id == user_id))
    u = res.scalar_one_or_none()
    if not u or not u.is_active:
        raise HTTPException(status_code=403, detail="User disabled")
    return u

@router.get("/me", response_model=MeOut)
async def me(current: User = Depends(get_current_user)):
    return MeOut(id=current.id, email=current.email, is_active=current.is_active, role=current.role)

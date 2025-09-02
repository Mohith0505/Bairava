from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt, JWTError

from app.infra.db import get_db
from app.domain.models.user import User
from app.domain.schemas.auth import SignupIn, LoginIn, TokenOut
from app.core.security import hash_password, verify_password, create_access_token
from app.config import settings

router = APIRouter()

@router.post("/signup", response_model=dict)
async def signup(payload: SignupIn, db: AsyncSession = Depends(get_db)):
    # check existing
    res = await db.execute(select(User).where(User.email == payload.email))
    if res.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    u = User(email=payload.email, hashed_password=hash_password(payload.password))
    db.add(u)
    await db.commit()
    return {"ok": True}

@router.post("/token", response_model=TokenOut)
async def token(payload: LoginIn, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(User).where(User.email == payload.email))
    u = res.scalar_one_or_none()
    if not u or not verify_password(payload.password, u.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    tok = create_access_token(str(u.id))
    return TokenOut(access_token=tok)

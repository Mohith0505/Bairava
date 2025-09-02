from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.routes.health import router as health_router
from app.api.routes import auth as auth_routes
from app.api.routes import users as users_routes
from app.infra.db import init_models

app = FastAPI(title=settings.APP_NAME, version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    await init_models()

@app.get("/")
async def root():
    return {"ok": True, "app": "Bairava API"}

# routers
app.include_router(health_router, prefix="/api", tags=["health"])
app.include_router(auth_routes.router, prefix="/api/auth", tags=["auth"])
app.include_router(users_routes.router, prefix="/api/users", tags=["users"])

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Bairava API"
    APP_ENV: str = "dev"
    APP_DEBUG: bool = True

    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"

    JWT_SECRET: str = "change-me-in-prod"
    JWT_EXPIRE_MIN: int = 60 * 24  # 24h

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

settings = Settings()

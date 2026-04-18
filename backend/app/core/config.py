from functools import lru_cache
from os import getenv

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    log_level: str = "INFO"
    cors_origins: str = "http://localhost:8080,http://127.0.0.1:8080,http://localhost:8089,http://127.0.0.1:8089,http://localhost:8090,http://127.0.0.1:8090"
    cors_origin_regex: str = (
        r"^https://php-client(?:-git-[a-z0-9-]+)?-[a-z0-9-]+\.vercel\.app$"
    )
    database_url: str = (
        "postgresql+psycopg://postgres:postgres@localhost:5432/events_db"
    )
    enable_in_memory_fallback: bool = False
    run_db_bootstrap: bool = False
    seed_events: bool = False
    seed_events_total: int = 10_000

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @model_validator(mode="after")
    def apply_runtime_defaults(self) -> "Settings":
        if getenv("VERCEL") == "1":
            self.app_env = getenv("VERCEL_ENV", "production")
            self.run_db_bootstrap = False
            self.seed_events = False
            if not getenv("DATABASE_URL"):
                self.enable_in_memory_fallback = True

        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()

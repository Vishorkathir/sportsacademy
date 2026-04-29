from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    project_name: str = "Cricket Academy Admission API"
    api_prefix: str = ""

    database_url: str
    auto_create_tables_on_startup: bool = True

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    auth_cookie_name: str = "access_token"
    auth_cookie_secure: bool = False
    auth_cookie_samesite: str = "lax"

    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding="utf-8", extra="ignore")


settings = Settings()

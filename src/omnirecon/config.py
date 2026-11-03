"""Application configuration; secrets are environment-only."""
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "OMNIRECON NEXUS X"
    app_env: str = "development"
    api_prefix: str = "/v1"
    log_level: str = "INFO"
    database_path: str = "data/omnirecon.db"
    model_base_url: str = ""
    model_api_key: str = ""
    model_name: str = ""
    model_timeout_seconds: float = 45.0

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()

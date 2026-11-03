"""Environment-backed application settings. Never put credentials in source control."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "OMNIRECON NEXUS X"
    app_env: str = "development"
    api_prefix: str = "/v1"
    log_level: str = "INFO"
    database_path: str = "data/omnirecon.db"
    model_timeout_seconds: float = 60.0
    provider_order: str = "openai,anthropic,google"

    openai_base_url: str = ""
    openai_api_key: str = ""
    openai_model: str = ""

    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-4-20250514"

    google_api_key: str = ""
    google_model: str = "gemini-2.5-flash"

    local_model_base_url: str = ""
    local_model_api_key: str = "local"
    local_model_name: str = ""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()

from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent
ENV_FILE_PATH = BASE_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH, env_file_encoding="utf-8")
    
    DEBUG: bool
    BOT_TOKEN: str

    BACKEND_URL: str
    BACKEND_API_KEY: str

    @computed_field  # type: ignore[misc]
    @property
    def backend_auth_header(self) -> dict:
        return {"Authorization": f"Api-Key {self.BACKEND_API_KEY}"}


settings = Settings()
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool
    BOT_TOKEN: str


settings = Settings()
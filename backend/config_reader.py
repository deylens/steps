from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = Path(__file__).parent.parent / ".env"


class Settings(BaseSettings):
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str

    model_config = SettingsConfigDict(env_file=DOTENV, env_file_encoding='utf-8')


db_config = Settings()

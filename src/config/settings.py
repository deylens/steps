from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    """Database settings configuration."""

    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: int
    driver: str

    model_config = SettingsConfigDict(
        env_file="db.env", env_file_encoding="utf-8", extra="ignore"
    )

    @property
    def db_url(self) -> str:
        return (
            f"{self.driver}://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


class AppConfig(BaseSettings):
    """Application settings configuration."""

    db: DBSettings = DBSettings()

    model_config = SettingsConfigDict(
        env_file="db.env", env_file_encoding="utf-8", extra="ignore"
    )


app_config = AppConfig()

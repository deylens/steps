from pydantic_settings import BaseSettings, SettingsConfigDict


DOTENV = ".env"


class DBSettings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: int
    driver: str

    model_config = SettingsConfigDict(env_file=DOTENV, env_file_encoding='utf-8', extra='ignore')

    @property
    def db_url(self):
        return (f"{self.driver}://{self.postgres_user}:"
                f"{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}")


db_config = DBSettings()

<<<<<<< HEAD
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = Path(__file__).resolve().parent.parent.parent / ".env"

class DBSettings(BaseSettings):
    db_user: str
    password: str
    name: str
    host: str
    port: int
    driver: str

    model_config = SettingsConfigDict(env_file=DOTENV, env_file_encoding='utf-8', extra='ignore')

    @property
    def get_url(self):
        return f"{self.driver}://{self.db_user}:{self.password}@{self.host}:{self.port}/{self.name}"

class DBTestSettings(BaseSettings):
    db_user_test: str
    password_test: str
    name_test: str
    host_test: str
    port_test: int
    driver_test: str

    model_config = SettingsConfigDict(env_file=DOTENV, env_file_encoding='utf-8', extra='ignore')

    @property
    def get_url(self):
        return f"{self.driver_test}://{self.db_user_test}:{self.password_test}@{self.host_test}:{self.port_test}/{self.name_test}"



db_config = DBSettings()
db_config_test = DBTestSettings()
=======
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: int
    driver: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')

    @property
    def db_url(self):
        return (f"{self.driver}://{self.postgres_user}:"
                f"{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}")


db_config = DBSettings()
>>>>>>> 5b2ecbb8756cc92dd5e988d30da3f83f04eee85e

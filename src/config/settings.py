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
        return f"{self.driver}://{self.db_user}:{self.password}@{self.host}:{self.port}/{self.name}"



db_config = DBSettings()
db_config_test = DBTestSettings()

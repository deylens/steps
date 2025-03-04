from pydantic_settings import BaseSettings, SettingsConfigDict


DOTENV = ".env"


class DBSettings(BaseSettings):
    db_user: str
    password: str
    name: str
    host: str
    port: int
    driver: str

    model_config = SettingsConfigDict(env_file=DOTENV, env_file_encoding='utf-8', extra='ignore')

    @property
    def db_url(self):
        return f"{self.driver}://{self.db_user}:{self.password}@{self.host}:{self.port}/{self.name}"


db_config = DBSettings()

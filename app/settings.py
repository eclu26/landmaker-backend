from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=None, extra="ignore")

    db_host: str
    db_port: int = 5432
    db_user: str
    db_password: str
    db_name: str

settings = Settings()
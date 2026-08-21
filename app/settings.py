from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=None, extra="ignore")

    db_host: str
    db_port: int = 5432
    db_user: str
    db_password: str
    db_name: str = "landmaker"

    s3_host: str
    s3_port: int = 9000
    s3_access_key: str
    s3_secret_key: str
    s3_region: str = "us-east-1"
    s3_bucket: str = "landmaker"

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expire_in_minutes: int = 60

settings = Settings()
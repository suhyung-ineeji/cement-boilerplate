from pydantic_settings import BaseSettings

class DBSettings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5678
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "postgres"

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"

db_settings = DBSettings()

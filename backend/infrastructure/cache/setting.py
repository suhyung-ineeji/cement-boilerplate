from pydantic_settings import BaseSettings
from pathlib import Path

class RedisSettings(BaseSettings):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = "1234"
    REDIS_DB: int = 0
    REDIS_POOL_MIN_CONNECTIONS: int = 1
    REDIS_POOL_MAX_CONNECTIONS: int = 10
    REDIS_POOL_TIMEOUT: int = 20
    REDIS_POOL_RETRY_ON_TIMEOUT: bool = True

    class Config:
        env_file = str(Path(__file__).resolve().parents[1] / ".env")
        env_file_encoding = "utf-8"
        extra = "ignore"
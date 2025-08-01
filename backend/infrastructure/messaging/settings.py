import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "guest"
    RABBITMQ_PASSWORD: str = "guest"
    RABBITMQ_VHOST: str = "/"

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"

rabbitmq_settings = Settings()

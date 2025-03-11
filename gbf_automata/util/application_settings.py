from pathlib import Path

from pydantic_settings import BaseSettings

env_path = Path(__file__).parent.parent / ".env"


class Settings(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 65432
    log_level: str = "INFO"
    log_format: str = "[%(asctime)s] [%(levelname)s] [%(thread)s] - %(message)s"

    class Config:
        env_file = env_path
        envi_file_encoding = "utf-8"


settings = Settings()

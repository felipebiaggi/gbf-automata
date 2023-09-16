from pydantic import Field, FilePath
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    display: str = Field(default=None)
    log_level: str = "INFO"
    log_format: str = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

    image_menu: str = Field(default=None)
    image_news: str = Field(default=None)
    image_home: str = Field(default=None)

    class Config:
        env_file = ".env"
        envi_file_encoding = "utf-8"


settings = Settings()       

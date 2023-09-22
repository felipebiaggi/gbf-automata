from pydantic import Field, field_validator
from pydantic_settings import BaseSettings
from gbf_automata.enums.content_type import ContentType
from typing import Union


class Settings(BaseSettings):
    display: str = Field(default=None)
    log_level: str = "INFO"
    log_format: str = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

    image_menu: str = Field(default=None)
    image_news: str = Field(default=None)
    image_home: str = Field(default=None)
    image_home_default: str = Field(default=None)
    image_back: str = Field(default=None)
    image_reload: str = Field(default=None)
    image_arcarum: str = Field(default=None)
    image_gw: str = Field(default=None)

    image_button_classic: str = Field(default=None)
    image_button_sandbox: str = Field(default=None)

    content_type: Union[str, ContentType] = Field(default=None)

    @field_validator("content_type")
    def str_to_enum(cls, value: str) -> ContentType:
        for member in ContentType:
            if member.name.lower() == value.lower():
                return member
        raise TypeError("Invalid Enum")

    class Config:
        env_file = ".env"
        envi_file_encoding = "utf-8"


settings = Settings()
